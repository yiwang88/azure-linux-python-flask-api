#!/bin/bash
service ssh start
cp /opt/resolv.conf /etc/resolv.conf
python /opt/app/main.py
