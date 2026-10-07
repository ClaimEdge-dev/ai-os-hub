window.RRR_DATA = {
  project: {
    id: "RRR",
    name: "Rapid Roadside Repair",
    phone: "(815) 749-3811",
    phoneTel: "+18157493811",
    state: "Illinois",
    status: "PRIVATE BENCHMARK MODE / NOT OWNER-VERIFIED",
    benchmarkMode: true
  },
  truth: [
    {key:"public_name", label:"Business Name", value:"Rapid Roadside Repair", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"phone", label:"Phone", value:"(815) 749-3811", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"core_service", label:"Core Service", value:"Emergency mobile roadside + on-site repair", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"asset_scope", label:"Asset Scope", value:"Semi trucks + trailers + broad equipment scope", state:"OWNER-CONFIRM", publicEnabled:false},
    {key:"hours", label:"Hours Model", value:"Benchmark: 24/7 emergency availability", state:"BENCHMARK / PRIVATE", publicEnabled:false},
    {key:"service_area", label:"Service Area Model", value:"Benchmark: 50-mile core / up to 100-mile extended; I-55 / I-80 / I-355 focus", state:"BENCHMARK / PRIVATE", publicEnabled:false},
    {key:"rates", label:"Rate Model", value:"Benchmark: $150 call + $150/hr, 2-hour minimum", state:"BENCHMARK / PRIVATE", publicEnabled:false},
    {key:"fleet_terms", label:"Fleet Terms Model", value:"Benchmark: Net 30 after credit approval; configurable PO rules", state:"BENCHMARK / PRIVATE", publicEnabled:false},
    {key:"warranty", label:"Warranty Drafting Model", value:"Benchmark: 90-day parts & labor; written final terms required", state:"BENCHMARK / PRIVATE", publicEnabled:false},
    {key:"credentials", label:"Credentials", value:"Licenses / insurance / certifications still require actual evidence", state:"HOLD", publicEnabled:false}
  ],
  services: [
    {id:"SVC-ROAD", family:"Emergency Roadside", label:"Emergency Roadside Assistance", description:"Breakdown triage and roadside repair intake.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-DIESEL", family:"Mobile Diesel / Mechanical", label:"Mobile Truck Repair", description:"Mechanical, starting, cooling, fuel, belts and hoses categories.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-ELEC", family:"Electrical / Diagnostics", label:"Electrical & Diagnostics", description:"Electrical, charging, fault-code and diagnostic categories.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-AIR", family:"Air / Brake", label:"Air & Brake Repair", description:"Air-line, leak and brake-system repair categories.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-TRAILER", family:"Trailer", label:"Mobile Trailer Repair", description:"Trailer electrical, air, brake, suspension, landing gear and hardware categories.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-TIRE", family:"Tire / Wheel", label:"Tire & Wheel Service", description:"Tire, wheel and hub categories when equipment/vendor support is confirmed.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-EMISS", family:"Aftertreatment", label:"DPF / DEF / Aftertreatment", description:"Fault diagnosis or regen when tools and capability are verified.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-HYD", family:"Hydraulics", label:"Mobile Hydraulic Service", description:"Field hydraulic diagnosis/repair benchmark category.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-WELD", family:"Welding / Fabrication", label:"Mobile Welding / Fabrication", description:"Roadside or job-site fabrication benchmark category.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-HEAVY", family:"Heavy Equipment", label:"Heavy Equipment Service", description:"On-site equipment repair for confirmed classes.", state:"BENCHMARK / PRIVATE"},
    {id:"SVC-FLEET", family:"Fleet / PM", label:"Fleet Maintenance", description:"Scheduled yard service and preventive-maintenance benchmark category.", state:"BENCHMARK / PRIVATE"}
  ],
  benchmarks: [
    {id:"BM-HOURS", label:"Emergency Availability", value:"24/7", range:"Regional mobile-roadside norm", note:"Private assumption only"},
    {id:"BM-AREA", label:"Service Radius", value:"50-mile core", range:"Up to 100-mile extended", note:"Planning anchor: Joliet/Channahon freight corridor, not an RRR address"},
    {id:"BM-CALL", label:"Standard Service Call", value:"$150", range:"Observed roughly $100-$235", note:"Not an official RRR price"},
    {id:"BM-LABOR", label:"Mobile Labor", value:"$150/hr", range:"Observed roughly $120-$180+", note:"2-hour working minimum"},
    {id:"BM-AH", label:"After-Hours Call", value:"$200", range:"Some competitors use surcharge; some do not", note:"Working benchmark only"},
    {id:"BM-MILE", label:"Travel / Mileage", value:"$2.00/mile", range:"Observed $1-$2 or fuel surcharge", note:"Use only when mileage model applies"},
    {id:"BM-PARTS", label:"Parts Markup", value:"30%", range:"Mobile/heavy-duty references roughly 15-40%", note:"Midwest heavy-duty benchmark"},
    {id:"BM-FLEET", label:"Fleet Terms", value:"Net 30", range:"After credit approval", note:"PO/account rules configurable"},
    {id:"BM-WARR", label:"Warranty Draft", value:"90-day parts & labor", range:"Market examples vary widely", note:"Requires written final terms before use"},
    {id:"BM-PAY", label:"Payment Model", value:"Cards + EFS + Comdata + ACH/Zelle", range:"Fleet billing optional", note:"Actual processor/account setup still required"}
  ],
  benchmarkCalculator: {
    serviceCall: 150,
    afterHoursCall: 200,
    laborHourly: 150,
    laborMinimumHours: 2,
    mileageRate: 2,
    partsMarkupPct: 30
  },
  releaseChecks: [
    "Actual legal/public identity confirmed",
    "Actual public email/domain verified",
    "Actual base/location and service area confirmed",
    "Actual services, tools and technician capabilities verified",
    "Licenses / insurance / certifications evidenced",
    "Benchmark rates converted into approved RRR rate authority",
    "Payment accounts and fleet terms actually configured",
    "Warranty written and approved",
    "Production backend/auth connected",
    "Request/photo workflow tested end-to-end",
    "Owner approves production release"
  ]
};
