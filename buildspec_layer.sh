
PY_DIR='build_layer/python/lib/python2.7/site-packages'
mkdir -p $PY_DIR
pip install -r requirements.txt --no-deps -t $PY_DIR
cp -r porper $PY_DIR
cd build_layer
zip -r ../porper_layer.zip .
cd ..
rm -r build_layer
aws lambda publish-layer-version --layer-name porper --zip-file fileb://porper_layer.zip
rm porper_layer.zip

# add this layer to a lambda function
#aws lambda update-function-configuration --function-name porper_with_layer --layers arn:aws:lambda:us-east-1:546276914724:layer:porper:6
