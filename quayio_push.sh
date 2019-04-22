#!/bin/bash
echo "$QUAY_PASSWORD" | docker login -u "$QUAY_USERNAME" --password-stdin quay.io
docker push quay.io/quaa/ev-solar-divert