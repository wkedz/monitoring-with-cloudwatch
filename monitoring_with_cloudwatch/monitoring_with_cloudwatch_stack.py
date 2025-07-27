import os
from typing import Final

from aws_cdk import (
    Stack,
    Duration,
)

from aws_cdk import (
    aws_lambda,
    aws_sns,
    aws_sns_subscriptions,
    aws_cloudwatch,
    aws_cloudwatch_actions,
)

from constructs import Construct

WEBHOOK_URL: Final[str] = os.environ.get("WEBHOOK_URL", "")

class MonitoringWithCloudwatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if not WEBHOOK_URL:
            print("No webhook URL provided.")
            raise ValueError("Webhook URL not configured")


        web_hook_lambda = aws_lambda.Function(
            self,
            "WebHookLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            code=aws_lambda.Code.from_asset("services"),
            handler="hook.handler",
            environment={
                "WEBHOOK_URL": WEBHOOK_URL
            },
        )

        # Create SNS Topic and subscribe the Lambda function to it
        # This topic will be used to send notifications from CloudWatch alarms
        alarm_topic = aws_sns.Topic(
            self, "AlarmTopic", display_name="AlarmTopic", topic_name="AlarmTopic"
        )

        # Subscribe the Lambda function to the SNS topic
        # This allows the Lambda function to receive messages from the topic
        alarm_topic.add_subscription(
            aws_sns_subscriptions.LambdaSubscription(web_hook_lambda)
        )

        # Create a CloudWatch alarm that triggers when the custom metric exceeds a threshold
        alarm = aws_cloudwatch.Alarm(
            self,
            "ApiAlarm",
            metric=aws_cloudwatch.Metric(
                metric_name="custom-error",
                namespace="Custom",
                period=Duration.minutes(1),
                statistic="Sum",
            ),
            evaluation_periods=1,
            threshold=100,
        )        

        # Add the SNS topic as an action for the alarm
        # This means that when the alarm state changes, a message will be sent to the SNS
        # topic, which in turn will invoke the Lambda function
        # to send a notification to the configured webhook URL
        topic_action = aws_cloudwatch_actions.SnsAction(alarm_topic)
        alarm.add_alarm_action(topic_action)
        alarm.add_ok_action(topic_action)