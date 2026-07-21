const { createClient } = require('@sanity/client')
const fs = require('fs')
const path = require('path')

// Load credentials from the gitignored .env in the studio folder,
// so the token never has to live inside this (shareable) script.
const ENV_PATH = 'C:\\Users\\vedan\\Desktop\\Haili\\hailiya_ropes\\.env'
const env = {}
for (const line of fs.readFileSync(ENV_PATH, 'utf8').split(/\r?\n/)) {
  const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/)
  if (m) env[m[1]] = m[2]
}

const client = createClient({
  projectId: env.SANITY_PROJECT_ID || '15fxxqgw',
  dataset: env.SANITY_DATASET || 'production',
  token: env.SANITY_AUTH_TOKEN,
  apiVersion: '2021-10-21',
  useCdn: false,
})

const IMAGES = 'C:\\Users\\vedan\\Desktop\\Haili\\netlify_deploy\\images'
const PROD   = IMAGES + '\\products'

const products = [
  // MARINE
  { order:1,  category:'Marine',  name:'UHMWPE 12-Strand Single Braided Rope',   img: PROD+'\\uhmwpe-12strand.jpg',                     spec1Label:'Diameter Range',              spec1Value:'2mm – 30mm',       tags:['UHMWPE','Industrial','Ship Mooring','Towing'] },
  { order:2,  category:'Marine',  name:'Polyester 12-Strand Single Braided Rope', img: PROD+'\\marine-02_Ocean_R_D_Single_-p1-3.jpeg',   spec1Label:'Max Breaking Strength',       spec1Value:'26,690 kgf',       tags:['Polyester','Ships','Fisheries','Drilling'] },
  { order:3,  category:'Marine',  name:'Aramid 12-Strand Single Braided Rope',    img: PROD+'\\marine-02_Ocean_R_D_Single_-p1-2.jpeg',   spec1Label:'Max Breaking Strength',       spec1Value:'60,000 kgf',       tags:['Aramid','Defence','Ocean Engineering'] },
  { order:4,  category:'Marine',  name:'Vectran 12-Strand Single Braided Rope',   img: PROD+'\\marine-02_Ocean_R_D_Single_-p1-4.jpeg',   spec1Label:'Max Breaking Strength',       spec1Value:'55,900 kgf',       tags:['Vectran','Zero Creep','Low Elongation'] },
  { order:5,  category:'Marine',  name:'Aramid III 12-Strand Single Braided Rope',img: PROD+'\\marine-04_Others-p1-3.jpeg',              spec1Label:'Max Breaking Strength',       spec1Value:'83,110 kgf',       tags:['Aramid III','Aerospace','Defence'] },
  { order:6,  category:'Marine',  name:'Non-metallic Cable Grip Sleeving',         img: PROD+'\\marine-03_Non-metallic_Cabl-p1-1.jpeg',   spec1Label:'Cable Diameter',              spec1Value:'4mm – 30mm',       tags:['Marine','Insulation','Corrosion Proof'] },
  { order:7,  category:'Marine',  name:'Synthetic Grips',                          img: PROD+'\\synthetic-grips.jpg',                     spec1Label:'Working Load (max)',           spec1Value:'2,400 lb',         tags:['Kevlar','Vectran','No-tool Loops'] },
  { order:8,  category:'Marine',  name:'Fiber Chain Belt',                         img: PROD+'\\marine-04_Others-p1-1.jpeg',              spec1Label:'Safety Factor',               spec1Value:'4×',               tags:['UHMWPE','Lifting','-40°C to 70°C'] },
  { order:9,  category:'Marine',  name:'Umbilical Cable',                          img: PROD+'\\marine-04_Others-p1-2.jpeg',              spec1Label:'Application',                 spec1Value:'Marine Exploration',tags:['Deep-sea','Subsea','Custom'] },
  { order:10, category:'Marine',  name:'Submerged Buoy Rope',                      img: PROD+'\\marine-01_Submerged_Buoy_Ro-p1-1.jpeg',   spec1Label:'Max Breaking Strength',       spec1Value:'18,850 kgf',       tags:['UHMWPE','Aramid','Vectran','Deep-sea','Buoy'] },
  { order:11, category:'Marine',  name:'Nylon Buoy Rope',                          img: PROD+'\\nylon-rope.jpg',                           spec1Label:'Elongation at Break',         spec1Value:'26%–36%',          tags:['Nylon','Buoy Mooring','Scientific Research'] },
  { order:12, category:'Marine',  name:'Sailboat Rope',                            img: PROD+'\\sailboat-rope.jpg',                       spec1Label:'Max Breaking Strength',       spec1Value:'5,360 kgf',        tags:['Sailboat','Mooring','Sail Control','Coloured'] },
  { order:13, category:'Marine',  name:'Tow Rope',                                 img: PROD+'\\tow-rope-marine.jpg',                     spec1Label:'Max Breaking Strength',       spec1Value:'80,000 kgf',       tags:['Towing','Nylon','Polyester','Marine Recovery'] },
  { order:14, category:'Marine',  name:'Winch Rope',                               img: PROD+'\\winch-rope-1.jpg',                        spec1Label:'Max Breaking Strength',       spec1Value:'8,500 kgf',        tags:['Winch','Off-road','UHMWPE','Lightweight'] },
  { order:15, category:'Marine',  name:'Soft Shackle',                             img: PROD+'\\marine-marine-p11-1.png',                 spec1Label:'Max Breaking Strength',       spec1Value:'35,000 kgf',       tags:['UHMWPE','Shackle','Corrosion Free','Lightweight'] },
  { order:16, category:'Marine',  name:'Elastic Anchor Cable',                     img: PROD+'\\marine-marine-p12-1.png',                 spec1Label:'Elastic Rope Breaking Strength',spec1Value:'1,500 kgf',    tags:['Elastic','Mooring','Floating Platform','Self-recovering'] },
  // DEFENCE
  { order:1,  category:'Defence', name:'High-Strength UHMWPE Rope',                img: PROD+'\\uhmwpe-defence.jpg',                      spec1Label:'Max Breaking Strength',       spec1Value:'823 tons',         tags:['UHMWPE','Anti-Rebound','Mooring','Anchorage'] },
  { order:2,  category:'Defence', name:'Polyamide Rope',                            img: PROD+'\\def-p5-1.png',                            spec1Label:'Application',                 spec1Value:'Ship Mooring & Towing',tags:['Polyamide','Corrosion Resistant','Naval'] },
  { order:3,  category:'Defence', name:'Fast Rope',                                 img: PROD+'\\fast-rope.png',                           spec1Label:'Breaking Strength (45mm)',    spec1Value:'15.1 tons',        tags:['Special Forces','Helicopter','Rapid Insertion'] },
  { order:4,  category:'Defence', name:'Combat Training System',                    img: PROD+'\\combat-training.jpg',                     spec1Label:'Standards',                   spec1Value:'EN892 / EN1891 / EN564',tags:['Defence Training','EN892','EN1891','Climbing'] },
  { order:5,  category:'Defence', name:'Tow Rope',                                  img: PROD+'\\def-p4-1.png',                            spec1Label:'Max Strength (Aramid)',        spec1Value:'65 tons',          tags:['Armored Vehicles','Tank Recovery','Field Ops'] },
  { order:6,  category:'Defence', name:'Soft Shackles',                             img: PROD+'\\def-p5-6.png',                            spec1Label:'Max Breaking Strength',       spec1Value:'100 tons',         tags:['UHMWPE','Corrosion Free','High Strength'] },
  { order:7,  category:'Defence', name:'Fireproof Rope',                            img: PROD+'\\fire-rope.png',                           spec1Label:'Diameter Options',            spec1Value:'8mm, 9.5mm, 12.5mm',tags:['Aramid','Fire Rescue','High Temperature'] },
  { order:8,  category:'Defence', name:'Ship Towing Rope',                          img: PROD+'\\ship-towing.jpg',                         spec1Label:'Application',                 spec1Value:'Naval Towing Operations',tags:['Naval','Ship Towing','High Strength'] },
  { order:9,  category:'Defence', name:'Synthetic Chain',                           img: PROD+'\\defence-Defence-p8-2.jpeg',               spec1Label:'Weight vs Steel Chain',       spec1Value:'85% lighter',      tags:['UHMWPE','Anchor','Mooring','Lightweight'] },
  { order:10, category:'Defence', name:'Aramid Rope',                               img: PROD+'\\defence-Defence-p9-1.jpeg',               spec1Label:'Max Breaking Strength',       spec1Value:'64 tons',          tags:['Aramid','Heat Resistant','Defence','Ocean Engineering'] },
  { order:11, category:'Defence', name:'Vectran Rope',                              img: PROD+'\\defence-Defence-p9-3.jpeg',               spec1Label:'Max Breaking Strength',       spec1Value:'60 tons',          tags:['Vectran','Zero Creep','Low Elongation','UV Resistant'] },
  { order:12, category:'Defence', name:'Aramid III Rope',                           img: PROD+'\\defence-Defence-p9-4.jpeg',               spec1Label:'Max Breaking Strength',       spec1Value:'83 tons',          tags:['Aramid III','Aerospace','Ultra High Strength','Extreme Environments'] },
  // SAFETY
  { order:1,  category:'Safety',  name:'“Jiaolong” Rope Rescue Technology System', img: IMAGES+'\\safety-jiaolong-rescue-system.png', spec1Label:'Capability', spec1Value:'Full Rescue Platform', tags:['Rescue Technology','Training','Emergency'] },
  { order:2,  category:'Safety',  name:'Static Rope (EN1891)',                      img: PROD+'\\static-rope-en1891.jpg',                  spec1Label:'Max Breaking Strength',       spec1Value:'42 kN',            tags:['EN1891','Nylon','Low Elongation'] },
  { order:3,  category:'Safety',  name:'Dynamic Rope (EN892)',                      img: PROD+'\\dynamic-rope-en892.jpg',                  spec1Label:'Dynamic Elongation',          spec1Value:'35–38%',           tags:['EN892','Energy Absorption','Fall Arrest'] },
  { order:4,  category:'Safety',  name:'Emergency Evacuation & Lifting System',     img: IMAGES+'\\safety-emergency-evacuation-lifting.png',spec1Label:'Capacity',                   spec1Value:'4–8 People',       tags:['Helicopter Evacuation','Weapons Lift'] },
  { order:5,  category:'Safety',  name:'Accessory Cord (EN564)',                    img: PROD+'\\accessory-cord.png',                      spec1Label:'Max Breaking Strength',       spec1Value:'16.9 kN',          tags:['EN564','Accessory','Personal Protection'] },
  { order:6,  category:'Safety',  name:'Rescue Training Scene Development',         img: IMAGES+'\\safety-rescue-training-scene.png',      spec1Label:'Type',                        spec1Value:'Turnkey Solution',  tags:['Infrastructure','Training','Emergency Services'] },
  { order:7,  category:'Safety',  name:'Throwline',                                 img: PROD+'\\throwline.jpg',                           spec1Label:'Max Breaking Strength',       spec1Value:'47.50 kN',         tags:['UHMWPE','Polypropylene','Water Rescue','NFPA'] },
  { order:8,  category:'Safety',  name:'Canyoning Rope',                            img: PROD+'\\canyoning-rope.jpg',                      spec1Label:'Max Breaking Strength',       spec1Value:'25.40 kN',         tags:['Canyoning','Cave Exploration','Wet Environment','Wear Resistant'] },
  { order:9,  category:'Safety',  name:'Lanyard',                                   img: PROD+'\\lanyard.jpg',                             spec1Label:'Breaking Strength',           spec1Value:'22 kN',            tags:['EN354','Personal Protection','Height Safety','Adjustable'] },
  { order:10, category:'Safety',  name:'Webbing',                                   img: PROD+'\\webbing.jpg',                             spec1Label:'Max Breaking Strength',       spec1Value:'35 kN',            tags:['EN566','EN795B','Polyester','UHMWPE','Height Safety'] },
  // OUTDOOR
  { order:1,  category:'Outdoor', name:'Dynamic Rope',                              img: PROD+'\\od-dynamic.jpg',                          spec1Label:'Max Impact Force',            spec1Value:'8.1 kN',           tags:['EN892','Falls','Climbing'] },
  { order:2,  category:'Outdoor', name:'Static Rope',                               img: PROD+'\\od-static.jpg',                           spec1Label:'Elongation at Break',         spec1Value:'2–3%',             tags:['EN1891','Rappelling','Low Stretch'] },
  { order:3,  category:'Outdoor', name:'Kinetic Recovery Rope',                     img: PROD+'\\od-kinetic.jpg',                          spec1Label:'Stretch',                     spec1Value:'20–30%',           tags:['Kinetic','Recovery','Off-road','4WD'] },
  { order:4,  category:'Outdoor', name:'Soft Shackle',                              img: IMAGES+'\\od_shackle1.jpg',                       spec1Label:'Breaking Strength',           spec1Value:'15,000 kgf',       tags:['UHMWPE','Lightweight','Corrosion Free'] },
  { order:5,  category:'Outdoor', name:'Winch Rope',                                img: IMAGES+'\\od_winch1.jpg',                         spec1Label:'Length',                      spec1Value:'30m standard',     tags:['UHMWPE','Off-road','Winch','Abrasion Resistant'] },
]

async function uploadImage(imgPath) {
  if (!fs.existsSync(imgPath)) { console.log(`  SKIP (missing): ${imgPath}`); return null }
  const ext = path.extname(imgPath).toLowerCase().replace('.','')
  const mime = ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : ext === 'png' ? 'image/png' : 'image/jpeg'
  return await client.assets.upload('image', fs.createReadStream(imgPath), {
    filename: path.basename(imgPath), contentType: mime
  })
}

async function run() {
  let done = 0, skipped = 0
  for (const p of products) {
    process.stdout.write(`Importing: ${p.name} ... `)
    const asset = await uploadImage(p.img)
    if (!asset) skipped++
    const doc = {
      _type: 'product',
      name: p.name,
      category: p.category,
      spec1Label: p.spec1Label,
      spec1Value: p.spec1Value,
      tags: p.tags,
      order: p.order,
    }
    if (asset) doc.image = { _type: 'image', asset: { _type: 'reference', _ref: asset._id } }
    await client.create(doc)
    done++
    console.log('done')
  }
  console.log(`\nAll products imported. Documents created: ${done}. Images missing/skipped: ${skipped}.`)
}

run().catch(console.error)
