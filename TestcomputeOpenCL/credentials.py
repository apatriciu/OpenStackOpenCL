#!/usr/bin/env python
import os

def get_nova_creds():
    d = {}
    d['username'] = "admin"
    d['api_key'] = "supersecret"
    d['auth_url'] = "http://192.168.2.22:35357/v2.0"
    d['project_id'] = "admin"
    return d


