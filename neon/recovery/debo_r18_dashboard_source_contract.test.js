'use strict';
const assert=require('node:assert/strict');
const {sourceHealth}=require('./debo_r18_dashboard_source_contract');
assert.equal(sourceHealth().health,'UNKNOWN');
assert.equal(sourceHealth({sourceReadVerified:true,taskReadsVerified:true}).eligible_for_release,false);
assert.equal(sourceHealth({sourceReadVerified:true,taskReadsVerified:true,acceptedCount:15,importReadbackVerified:false}).reason,'SYNC_NOT_VERIFIED');
assert.equal(sourceHealth({sourceReadVerified:true,taskReadsVerified:true,acceptedCount:15,importReadbackVerified:true}).reason,'MOBILE_QA_OPEN');
assert.equal(sourceHealth({sourceReadVerified:true,taskReadsVerified:true,acceptedCount:15,importReadbackVerified:true,mobileQAPassed:true}).eligible_for_release,true);
console.log('PASS 5 dashboard contract assertions');
