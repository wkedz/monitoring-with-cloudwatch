import aws_cdk as core
import aws_cdk.assertions as assertions

from monitoring_with_cloudwatch.monitoring_with_cloudwatch_stack import MonitoringWithCloudwatchStack

# example tests. To run these tests, uncomment this file along with the example
# resource in monitoring_with_cloudwatch/monitoring_with_cloudwatch_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MonitoringWithCloudwatchStack(app, "monitoring-with-cloudwatch")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
