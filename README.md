# Cloudwatch monitoring

Repository containg cdk code that will deploy CloudWatch monitoring, that will send alerts.

Those alerts will then be propagated to Slack using [weebhook](https://api.slack.com/messaging/webhooks)

## Define metric

We cannot modify aws namespaces metrics. We need to create them by ourselfs in custom namespaces. It can be done by command line `aws`

```bash
aws cloudwatch put-metric-data --namespace Custom --metric-name custom-error --value 1
```


Create alarm
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "Test alarm" \
  --namespace "Custom" \
  --metric-name "custom-error" \
  --statistic "Sum" \
  --period 60 \
  --threshold 100 \
  --comparison-operator "GreaterThanThreshold" \
  --evaluation-periods 1 \
  --unit "Count"
```

Get info about alarm

```bash
aws cloudwatch describe-alarms --alarm-names "Test alarm"
```

## Webhook url

In order this to work, you need to provide webook url throuh WEBHOOK_URL env variable.
