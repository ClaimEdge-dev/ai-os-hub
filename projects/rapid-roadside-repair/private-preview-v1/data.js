window.RRR_DATA = {
  project: {
    id: "RRR",
    name: "Rapid Roadside Repair",
    phone: "(815) 749-3811",
    phoneTel: "+18157493811",
    state: "Illinois",
    status: "PRIVATE PROTOTYPE / OWNER-TRUTH-GATED"
  },
  truth: [
    {key:"public_name", label:"Business Name", value:"Rapid Roadside Repair", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"phone", label:"Phone", value:"(815) 749-3811", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"core_service", label:"Core Service", value:"Emergency mobile roadside + on-site repair", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"asset_scope", label:"Asset Scope", value:"Semi trucks + trailers + broad equipment scope", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"hours", label:"24/7 / Hours", value:"Not verified", state:"HOLD", publicEnabled:false},
    {key:"service_area", label:"Service Area", value:"Exact radius / counties / corridors not verified", state:"HOLD", publicEnabled:false},
    {key:"rates", label:"Rates", value:"No official Rapid rate card loaded", state:"HOLD", publicEnabled:false},
    {key:"credentials", label:"Credentials", value:"Licenses / insurance / certifications need evidence", state:"HOLD", publicEnabled:false}
  ],
  services: [
    {id:"SVC-ROAD", family:"Emergency Roadside", label:"Emergency Roadside Assistance", description:"Breakdown triage and roadside repair intake.", state:"OWNER-CONFIRM"},
    {id:"SVC-DIESEL", family:"Mobile Diesel / Mechanical", label:"Mobile Truck Repair", description:"Mechanical, starting, cooling, fuel, belts and hoses categories.", state:"OWNER-CONFIRM"},
    {id:"SVC-ELEC", family:"Electrical / Diagnostics", label:"Electrical & Diagnostics", description:"Electrical, charging, fault-code and diagnostic categories.", state:"OWNER-CONFIRM"},
    {id:"SVC-AIR", family:"Air / Brake", label:"Air & Brake Repair", description:"Air-line, leak and brake-system repair categories.", state:"OWNER-CONFIRM"},
    {id:"SVC-TRAILER", family:"Trailer", label:"Mobile Trailer Repair", description:"Trailer electrical, air, brake, suspension, landing gear and hardware categories.", state:"OWNER-CONFIRM"},
    {id:"SVC-TIRE", family:"Tire / Wheel", label:"Tire & Wheel Service", description:"Tire, wheel and hub categories when equipment/vendor support is confirmed.", state:"HOLD"},
    {id:"SVC-EMISS", family:"Aftertreatment", label:"DPF / DEF / Aftertreatment", description:"Fault diagnosis or regen only when tools and capability are verified.", state:"HOLD"},
    {id:"SVC-HYD", family:"Hydraulics", label:"Mobile Hydraulic Service", description:"Field hydraulic diagnosis/repair when equipment and parts support are verified.", state:"HOLD"},
    {id:"SVC-WELD", family:"Welding / Fabrication", label:"Mobile Welding / Fabrication", description:"Roadside or job-site fabrication when actual welding capability is verified.", state:"HOLD"},
    {id:"SVC-HEAVY", family:"Heavy Equipment", label:"Heavy Equipment Service", description:"On-site equipment repair for owner-confirmed classes.", state:"OWNER-CONFIRM"},
    {id:"SVC-FLEET", family:"Fleet / PM", label:"Fleet Maintenance", description:"Scheduled yard service and preventive maintenance when approved.", state:"OWNER-CONFIRM"}
  ],
  releaseChecks: [
    "Billy confirms public business name and phone",
    "Public email/domain verified",
    "Hours / 24-7 claim verified",
    "Service area verified",
    "Public services and exclusions approved",
    "Equipment/tools and credentials verified",
    "Approved rate authority loaded",
    "Privacy/legal terms reviewed",
    "Production backend/auth connected",
    "Request/photo workflow tested end-to-end",
    "Owner approves production release"
  ]
};
