
source .env.local

mkdir -p src/$PYTHON_FOLDER
cp -r porper src/$PYTHON_FOLDER
cd src; pip install -r requirements.txt --no-deps -t $PYTHON_FOLDER; cd ..

aws cloudformation package \
   --template-file ./template.yaml \
   --s3-bucket $S3_BUCKET_NAME \
   --output-template-file samTemplate.yaml

aws cloudformation deploy --template-file ./samTemplate.yaml \
  --capabilities CAPABILITY_IAM \
  --stack-name SungardAS-porper-core \
  --parameter-overrides \
    ReadCapacityUnit=$READ_CAPACITY_UNIT \
    WriteCapacityUnit=$WRITE_CAPACITY_UNIT

rm -rf src/$PYTHON_FOLDER
