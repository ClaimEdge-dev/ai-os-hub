export const TEAM_TRUTH=Object.freeze({
  OFFICIAL:"OFFICIAL",
  DEMO:"DEMO",
  NEEDS_COACH_CONFIRMATION:"NEEDS_COACH_CONFIRMATION"
});

export function canRelease(item,audience){
  if(!item) return {ok:false,reason:"missing_item"};
  if(item.team_truth_state!==TEAM_TRUTH.OFFICIAL) return {ok:false,reason:"not_official"};
  if(!item.coach_approved) return {ok:false,reason:"not_coach_approved"};
  if(audience==="PLAYER" && item.coach_only) return {ok:false,reason:"coach_only"};
  return {ok:true};
}
