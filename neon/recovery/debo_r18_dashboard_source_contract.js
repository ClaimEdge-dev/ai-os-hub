'use strict';
// Pure dashboard-source health projection. No private task data in feed.
function sourceHealth({sourceReadVerified=false,taskReadsVerified=false,latestReadAt=null,acceptedCount=0,importReadbackVerified=false,mobileQAPassed=false}={}) {
 const synchronized=sourceReadVerified && taskReadsVerified && importReadbackVerified && acceptedCount>0;
 return Object.freeze({source:'DEBO Core',health:synchronized?'VERIFIED':'UNKNOWN',read_at:latestReadAt,
  eligible_for_release:Boolean(synchronized&&mobileQAPassed),
  reason:!sourceReadVerified?'SOURCE_NOT_VERIFIED':!taskReadsVerified?'CORE_READBACK_MISSING':!importReadbackVerified?'SYNC_NOT_VERIFIED':!mobileQAPassed?'MOBILE_QA_OPEN':'ACCEPTED'});
}
module.exports={sourceHealth};
