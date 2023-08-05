from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_value_check import BaseResourceValueCheck


class KinesisStreamEncryptionType(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure Kinesis Stream is securely encrypted"
        id = "CKV_AWS_43"
        supported_resources = ['AWS::Kinesis::Stream']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return 'Properties/StreamEncryption/EncryptionType'

    def get_expected_value(self):
        return 'KMS'


check = KinesisStreamEncryptionType()
