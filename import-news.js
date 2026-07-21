const { createClient } = require('@sanity/client')
const fs = require('fs')

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

const articles = [
  ["index167","2026-05-14","Why Does Knotting a Webbing Reduce Strength More Than Knotting a Rope?","For professionals in high-altitude work, rock climbing, and rescue operations, understanding the strength loss caused by knots is critical. Round rope retains 60–80% strength when knotted; webbing drops to just 30–45%.","Safety"],
  ["index166","2026-05-12","IRATA vs DRT — What's the Difference and How Do They Work Together?","For professionals in high-altitude work, terms like IRATA and DRT are often mentioned together. DRT is a safety technique, while IRATA is the organization that turns it into a global industrial standard.","Industry"],
  ["index165","2026-05-09","When Rescue Missions Become More Dangerous, Rope Reliability Becomes Critical","As rescue environments grow more demanding — from high-rise urban incidents to technical mountain rescues — the ropes that teams rely on must perform without compromise.","Safety"],
  ["index164","2026-05-07","What is IRATA?","IRATA (Industrial Rope Access Trade Association) is the global standard-setting body for industrial rope access and rope safety certification worldwide.","Industry"],
  ["index163","2026-04-27","Is Your Rope Ready for When Things Go Wrong?","Every rope is engineered, tested, and certified to perform under extreme load, friction, and environmental stress. Know the signs of a compromised rope before it's too late.","Safety"],
  ["index162","2026-04-24","The Most Dangerous Mistake Isn't the Environment — It's the Wrong Choice","Choosing the wrong rope for a mission doesn't just risk failure — it risks lives. The margin for error in defence and rescue operations is zero.","Defence"],
  ["index161","2026-04-21","Sailboat Rope Basics — Materials, Classification & Maintenance","Modern sailing ropes use UHMWPE, Vectran®, and PBO fibers. Learn how to classify halyards, sheets, control lines, standard colour coding, and maintenance guidelines.","Marine"],
  ["index160","2026-04-18","How to Choose an Air Conditioner Installation Safety Rope?","Air-conditioner installation is one of the most common high-risk trades worldwide. Three non-negotiable parameters: breaking strength, elongation, and diameter.","Safety"],
  ["index159","2026-04-14","Jiaolong PRAC Coach Training Concludes Successfully in Kuala Lumpur","From March 30 to April 5, 2026, a high-level Jiaolong delegation conducted exclusive PRAC Coach Training in Kuala Lumpur. Eight participants earned PRAC Coach credentials.","Company"],
  ["index158","2026-04-09","When the Environment Changes, Your Rope Must Adapt!","Strong winds, wet surfaces, UV exposure, saltwater, extreme cold — modern rope applications face all of these simultaneously.","Marine"],
  ["index156","2026-04-03","Is Your Rope Ready for When Things Go Wrong? (II)","Can your rope handle failure, stress, and the unexpected? Every rope is engineered, tested, and certified to perform under extreme load, friction, and environmental stress.","Safety"],
  ["index155","2026-03-30","The Haili Story (Part II): Breaking Through and Reborn","How much weight can a single rope bear? How many legends can a century-old factory continue to write? The remarkable story of Hailiya's rebirth.","Company"],
  ["index154","2026-03-25","When the Mountain Crumbles: Lessons from the Jiangxi Rappelling Tragedy","Following the Jiangxi rappelling tragedy where limestone rockfall claimed three lives: in high-risk environments, certified dynamic rope isn't optional — it's survival.","Safety"],
  ["index153","2026-03-18","The Story of Haili (Part 1): A Century of Trials","In 1923, a red string woven in Qingdao gave birth to Xiecheng Lace Factory — later known as Hailiya. A century of innovation begins here.","Company"],
  ["index152","2026-03-17","10.5mm Integral Core-Sheath Static Rope","The 10.5mm bonded sheath rope, with its perfect combination of high-strength nylon and polyester fibers, exhibits extremely low elongation and exceptional performance.","Marine"],
  ["index151","2026-03-12","Is Your Lifeline Compromised? 2026 Safety Recalls","Understanding the 2026 safety recall landscape and what it means for rope system selection, inspection, and compliance in professional applications.","Safety"],
  ["index150","2026-03-07","Patent New Product: Huakai Four-Claw Rope","Huakai's patented Four-Claw Rope represents a breakthrough in cable pulling safety, reducing operator risk and improving efficiency in cable installation.","Company"],
  ["index149","2026-02-27","Building Unity Through Collaboration, Securing Safety Through Practice","Jiaolong's cross-departmental training program strengthens team cohesion and technical proficiency across rescue operations, field tactics, and equipment deployment.","Company"],
  ["index148","2026-02-25","Qingdao Huakai (Hailiya Group) Celebrate 2026 Chinese New Year","Singing and Dancing: A Cultural Feast Warmly Concludes the 2026 Chinese New Year Annual Meeting Gala.","Company"],
  ["index147","2026-02-06","Comprehensive Analysis of Sailing Rope Systems","An in-depth guide covering material properties of UHMWPE, Vectran®, and polyester sailing ropes, with selection criteria and care protocols.","Marine"],
  ["index146","2026-02-02","How Our Fast Rope Delivers High Performance for Tactical Operations","High-performance Fast Rope designed for rapid tactical and rescue operations, offering exceptional strength, heat resistance, and controlled grip.","Defence"],
  ["index145","2026-01-23","Major Certification! Hailiya Group's Escape Descent Device Selected for National Industrial Safety Catalog","Selected for China's national industrial safety equipment catalog — Hailiya Group's escape descent device, co-developed with Tsinghua University.","Company"],
  ["index144","2026-01-15","Rope Redefined: The Unsung Hero of Every Great Voyage","Modern sailboat rope is a high-tech marvel, engineered from advanced fibers for minimal stretch, lightweight performance, and durability in ocean racing.","Marine"],
  ["index143","2026-01-09","Hailiya Group Rushes to Fire Site to Carry Out Emergency Rescue","Hailiya Group's emergency team quickly responded to a fire at a Qingdao centre, demonstrating professional rescue capability.","Company"],
  ["index142","2025-12-31","Hailiya Group Celebrate New Year — Happy New Year 2026!","Happy New Year 2026! We look forward to building a stronger future of cooperation — a year of innovation, global expansion, and product excellence.","Company"],
  ["index141","2025-12-01","Delegation from Ceuta Autonomous City Fire Service, Spain, Visits Hailiya Group","The Ceuta Fire Service visited Hailiya Group for an exchange, engaging in in-depth cooperation regarding the Jiaolong rope rescue equipment system.","Company"],
  ["index140","2025-11-27","National Pride! Hailiya Group's 'Jiaolong' Invited as Rope Supplier for GRIMPDAY","Hailiya's Jiaolong brand selected as official rope supplier for the prestigious GRIMPDAY International Rope Technology Competition.","Company"],
  ["index139","2025-11-24","Jiaolong Contributes to the 2025 GRIMPDAY CHINA International Competition","From Nov 16–19, 2025 GRIMPDAY CHINA competition took place in Ruyuan, Shaoguan. Hailiya Group's Jiaolong served as official rope supplier.","Company"],
  ["index138","2025-11-20","Pacific Island Nations Climate Change Workshop Delegation Visits Hailiya Group","The Pacific Island Nations Climate Change and Disaster Risk Management Workshop delegation conducted an inspection and exchange visit.","Company"],
  ["index137","2025-11-13","10.5mm Sheath-Core Fusion Static Rope — Product Introduction","Introduction to Hailiya's 10.5mm Sheath-Core Fusion Static Rope, featuring advanced bonding technology and EN1891 compliance.","Marine"],
  ["index50","2025-08-28","What is the Difference Between Jiaolong Static Rope and Low Stretch Kernmantle Rope?","Clarifying the difference between Jiaolong's standard static rope and their low-stretch kernmantle rope — construction, elongation, and use case.","Safety"],
  ["index49","2023-08-23","Outdoor Retailer Summer Market 2023 — Hailiya Group Participates","Hailiya Group's participation in Outdoor Retailer Summer Market 2023 — showcasing Jiaolong climbing and outdoor rope systems to global buyers.","Company"],
  ["index48","2022-08-12","New Website of Qingdao Huakai Rope Is Online Now","New window, new face to the world — Qingdao Huakai Ocean Science and Technology launches its new official website for global customers.","Company"],
]

async function run() {
  let done = 0, withImg = 0, noImg = 0
  for (const [id, date, title, excerpt, category] of articles) {
    process.stdout.write(`Importing: ${title.slice(0,50)}... `)
    const imgPath = IMAGES + '\\news_' + id + '.jpg'
    let imageRef = null
    if (fs.existsSync(imgPath)) {
      const asset = await client.assets.upload('image', fs.createReadStream(imgPath), {
        filename: 'news_' + id + '.jpg', contentType: 'image/jpeg'
      })
      imageRef = { _type: 'image', asset: { _type: 'reference', _ref: asset._id } }
      withImg++
    } else {
      noImg++
    }
    const doc = { _type: 'newsArticle', title, date, category, excerpt }
    if (imageRef) doc.thumbnail = imageRef
    await client.create(doc)
    done++
    console.log(imageRef ? 'done' : 'done (no thumbnail)')
  }
  console.log(`\nAll news articles imported. Documents created: ${done}. With thumbnail: ${withImg}. No thumbnail: ${noImg}.`)
}

run().catch(console.error)
