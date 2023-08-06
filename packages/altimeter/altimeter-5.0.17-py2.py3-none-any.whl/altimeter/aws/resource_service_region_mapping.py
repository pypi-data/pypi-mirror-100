"""Discover service/region availability"""
from collections import defaultdict
import random
from typing import DefaultDict, Dict, Tuple, Type

import boto3
from pydantic import BaseModel

from altimeter.aws.scan.settings import ALL_RESOURCE_SPEC_CLASSES
from altimeter.aws.resource.resource_spec import AWSResourceSpec, ScanGranularity
from altimeter.core.log import Logger
from altimeter.aws.log_events import AWSLogEvents


class NoRegionsFoundForResource(Exception):
    """Indicates no regions could be found for a resource"""


class AWSResourceRegionMappingRepository(BaseModel):
    """Contains the mappings between AWS resources and regions"""

    boto_service_resource_region_mappings: Dict[str, Dict[str, Tuple[str, ...]]]

    def get_regions(
        self, resource_spec_class: Type[AWSResourceSpec], region_whitelist: Tuple[str, ...]
    ) -> Tuple[str, ...]:
        logger = Logger()
        with logger.bind(resource_spec_class=resource_spec_class):
            logger.info(event=AWSLogEvents.GetServiceResourceRegionMappingStart)
            service = resource_spec_class.service_name
            resource = resource_spec_class.type_name
            prefiltered_regions = self.boto_service_resource_region_mappings.get(service, {}).get(
                resource, ()
            )
            if region_whitelist:
                regions = tuple(
                    region for region in prefiltered_regions if region in region_whitelist
                )
            else:
                regions = prefiltered_regions
            if not regions:
                raise NoRegionsFoundForResource(
                    f"No regions found for resource {service}/{resource}"
                )
            logger.info(event=AWSLogEvents.GetServiceResourceRegionMappingEnd)
            return regions


def build_aws_resource_region_mapping_repo(
    global_region_whitelist: Tuple[str, ...],
    preferred_account_scan_regions: Tuple[str, ...],
    resource_spec_classes: Tuple[Type[AWSResourceSpec], ...] = ALL_RESOURCE_SPEC_CLASSES,
) -> "AWSResourceRegionMappingRepository":
    """Build mappings representing the region availability of AWS Resources.

    Args:
        global_region_whitelist: if populated this is used as a region whitelist
        preferred_account_scan_regions: regions which should be used for Account granularity resources
        resource_spec_classes: AWSResourceSpec classes to include in the mappings

    Returns:
        AWSResourceRegionMappingRepository
    """
    services = tuple(
        resource_spec_class.service_name for resource_spec_class in resource_spec_classes
    )
    boto_service_region_mappings = get_boto_service_region_mapping(services=services)
    boto_service_resource_region_mappings: DefaultDict[
        str, Dict[str, Tuple[str, ...]]
    ] = defaultdict(dict)
    for resource_spec_class in resource_spec_classes:
        resource_name = resource_spec_class.type_name
        service_name = resource_spec_class.service_name
        candidate_regions = boto_service_region_mappings.get(service_name, ())
        if "aws-global" in candidate_regions:
            if resource_spec_class.scan_granularity != ScanGranularity.ACCOUNT:
                raise Exception(
                    f"BUG: boto mappings contain {resource_spec_class} "
                    f"region aws-global but class is marked {resource_spec_class.scan_granularity} granularity"
                )
            candidate_regions = preferred_account_scan_regions
        if resource_spec_class.region_whitelist:
            candidate_regions = tuple(
                region
                for region in resource_spec_class.region_whitelist
                if region in candidate_regions
            )
        if global_region_whitelist:
            candidate_regions = tuple(
                region for region in candidate_regions if region in global_region_whitelist
            )
        if resource_spec_class.scan_granularity == ScanGranularity.ACCOUNT:
            if candidate_regions:
                candidate_regions = tuple(
                    region
                    for region in candidate_regions
                    if region in preferred_account_scan_regions
                )
                if candidate_regions:
                    candidate_regions = (random.choice(candidate_regions),)
        boto_service_resource_region_mappings[service_name][resource_name] = candidate_regions
    return AWSResourceRegionMappingRepository(
        boto_service_resource_region_mappings=boto_service_resource_region_mappings,
    )


def get_boto_service_region_mapping(services: Tuple[str, ...]) -> Dict[str, Tuple[str, ...]]:
    """Return a mapping of service names to supported regions for the given services using boto"""
    service_region_mapping: Dict[str, Tuple[str, ...]] = {}
    session = boto3.Session()
    for service in services:
        service_region_mapping[service] = tuple(
            session.get_available_regions(service_name=service, allow_non_regional=True)
        )
    return service_region_mapping
