#!/usr/bin/env node

"use strict";

require('console-stamp')(console, { pattern: 'HH:MM:ss.l', label: false });

const express = require('express');

const app = express();
app.use(express.static('./device/pi/midgard'));
app.listen(8888, () => console.log('shell listening on port 8888'));

