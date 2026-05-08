import boto3


class S3Storage:
    def __init__(
        self,
        endpoint_url: str,
        region: str,
        access_key: str,
        secret_key: str,
        bucket: str,
    ):
        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def ensure_bucket(self) -> None:
        existing = [b["Name"] for b in self.client.list_buckets().get("Buckets", [])]
        if self.bucket not in existing:
            self.client.create_bucket(Bucket=self.bucket)

    def upload_pdf(self, key: str, content: bytes) -> None:
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType="application/pdf",
        )

    def generate_presigned_url(self, key: str, expires_in: int) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires_in,
        )
