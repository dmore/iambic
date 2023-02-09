from __future__ import annotations

TEST_PAYLOAD = """{"version":"0","id":"40c8d15b-5d07-2a6f-fd21-450bf6415596","detail-type":"AWS API Call via CloudTrail","source":"aws.iam","account":"1234567890012","time":"2023-01-24T19:21:42Z","region":"us-east-1","resources":[],"detail":{"eventVersion":"1.08","userIdentity":{"type":"AssumedRole","principalId":"AROAWODXPQXPVK7IYR4VJ:noq_principal_updater_steven@noq.dev","arn":"arn:aws:sts::1234567890012:assumed-role/NoqSpokeRoleCorpNoqDev/noq_principal_updater_steven@noq.dev","accountId":"1234567890012","accessKeyId":"ASIAWODXPQXPSPZIOHJ3","sessionContext":{"sessionIssuer":{"type":"Role","principalId":"AROAWODXPQXPVK7IYR4VJ","arn":"arn:aws:iam::1234567890012:role/NoqSpokeRoleCorpNoqDev","accountId":"1234567890012","userName":"NoqSpokeRoleCorpNoqDev"},"webIdFederationData":{},"attributes":{"creationDate":"2023-01-24T18:59:38Z","mfaAuthenticated":"false"}}},"eventTime":"2023-01-24T19:21:42Z","eventSource":"iam.amazonaws.com","eventName":"TagRole","awsRegion":"us-east-1","sourceIPAddress":"54.71.102.1","userAgent":"Boto3/1.26.36 Python/3.10.6 Linux/4.14.301-224.520.amzn2.x86_64 exec-env/AWS_ECS_FARGATE Botocore/1.29.36","requestParameters":{"roleName":"test_detect_role","tags":[{"key":"test-tag","value":"detection-for-eventbridge-attempt-2"}]},"responseElements":null,"requestID":"5704926d-fe93-4a85-8440-8f29fd63fa5e","eventID":"07dcf958-5664-4de1-9ff4-99c76de89fb3","readOnly":false,"eventType":"AwsApiCall","managementEvent":true,"recipientAccountId":"1234567890012","eventCategory":"Management","tlsDetails":{"tlsVersion":"TLSv1.2","cipherSuite":"ECDHE-RSA-AES128-GCM-SHA256","clientProvidedHostHeader":"iam.amazonaws.com"}}}"""
