#!/bin/bash

pip install -e /openedx/requirements/iaa-xblock

cd /openedx/requirements/iaa-xblock
cp /openedx/edx-platform/setup.cfg .
mkdir test_root
cd test_root/
ln -s /openedx/staticfiles .

cd /openedx/requirements/iaa-xblock

DJANGO_SETTINGS_MODULE=lms.envs.test EDXAPP_TEST_MONGO_HOST=mongodb pytest iaaxblock/tests.py

rm -rf test_root