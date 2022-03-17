#!/usr/bin/env python3
import logging
import sys
import yaml
import json

cr = sys.stdin
parsed_cr = yaml.safe_load(cr.read())
manifest = parsed_cr.get('object')
phase = manifest.get('status',{}).get('phase', {})
if not phase or phase != 'completed':
    logging.info('updating status')
    manifest['status'] = {}
    manifest['status']['phase'] = 'completed'
updated_cr = sys.stdout
updated_cr.write(json.dumps(parsed_cr))