"""
scrape_build_news.py
Fetches every article page from hailiya.com.au, downloads thumbnail images,
then rewrites the news section in index.html with all 119 articles,
self-contained pagination (no external links), and in-page article viewer.
"""
import sys, os, re, json, time, urllib.request, urllib.error, html as html_module
sys.stdout.reconfigure(encoding='utf-8')

HTML_PATH  = r"C:\Users\vedan\Desktop\Haili\index.html"
IMG_DIR    = r"C:\Users\vedan\Desktop\Haili\images"
BASE_URL   = "https://www.hailiya.com.au"

# ── All 119 articles collected from all 12 listing pages ──────────────────────
ALL_ARTICLES = [
    # Page 1
    ("index167","2026-05-14","Why Does Knotting a Webbing Reduce Strength More Than Knotting a Rope?","For professionals in high-altitude work, rock climbing, and rescue operations, understanding the strength loss caused by knots is critical. Round rope retains 60–80% strength when knotted; webbing drops to just 30–45%.","Safety"),
    ("index166","2026-05-12","IRATA vs DRT — What's the Difference and How Do They Work Together?","For professionals in high-altitude work, terms like IRATA and DRT are often mentioned together. DRT is a safety technique, while IRATA is the organization that turns it into a global industrial standard.","Industry"),
    ("index165","2026-05-09","When Rescue Missions Become More Dangerous, Rope Reliability Becomes Critical","As rescue environments grow more demanding — from high-rise urban incidents to technical mountain rescues — the ropes that teams rely on must perform without compromise.","Safety"),
    ("index164","2026-05-07","What is IRATA?","IRATA (Industrial Rope Access Trade Association) is the global standard-setting body for industrial rope access and rope safety certification worldwide.","Industry"),
    ("index163","2026-04-27","Is Your Rope Ready for When Things Go Wrong?","Every rope is engineered, tested, and certified to perform under extreme load, friction, and environmental stress. Know the signs of a compromised rope before it's too late.","Safety"),
    ("index162","2026-04-24","The Most Dangerous Mistake Isn't the Environment — It's the Wrong Choice","Choosing the wrong rope for a mission doesn't just risk failure — it risks lives. The margin for error in defence and rescue operations is zero.","Defence"),
    ("index161","2026-04-21","Sailboat Rope Basics — Materials, Classification & Maintenance","Modern sailing ropes use UHMWPE, Vectran®, and PBO fibers. Learn how to classify halyards, sheets, control lines, standard colour coding, and maintenance guidelines.","Marine"),
    ("index160","2026-04-18","How to Choose an Air Conditioner Installation Safety Rope? 3 Key Parameters You Must Know","Air-conditioner installation is one of the most common high-risk trades worldwide. Three non-negotiable parameters: breaking strength, elongation, and diameter.","Safety"),
    ("index159","2026-04-14","Jiaolong PRAC Coach Training Concludes Successfully in Kuala Lumpur","From March 30 to April 5, 2026, a high-level Jiaolong delegation conducted exclusive PRAC Coach Training in Kuala Lumpur. Eight participants earned PRAC Coach credentials.","Company"),
    ("index158","2026-04-09","When the Environment Changes, Your Rope Must Adapt!","Strong winds, wet surfaces, UV exposure, saltwater, extreme cold — modern rope applications face all of these simultaneously. Huakai's fibre technology ensures consistent performance.","Marine"),
    # Page 2
    ("index156","2026-04-03","Is Your Rope Ready for When Things Go Wrong?","Can your rope handle failure, stress, and the unexpected? Every rope is engineered, tested, and certified to perform under extreme load, friction, and environmental stress.","Safety"),
    ("index155","2026-03-30","The Haili Story (Part II): Breaking Through and Reborn — Setting Sail Again After the Storm","How much weight can a single rope bear? How many legends can a century-old factory continue to write? The remarkable story of Hailiya's rebirth.","Company"),
    ("index154","2026-03-25","When the Mountain Crumbles: Lessons from the Jiangxi Rappelling Tragedy","Following the Jiangxi rappelling tragedy where limestone rockfall claimed three lives: in high-risk environments, certified dynamic rope isn't optional — it's survival.","Safety"),
    ("index153","2026-03-18","The Story of Haili (Part 1): A Century of Trials, Beginning with a Piece of Red String","In 1923, a red string woven in Qingdao gave birth to Xiecheng Lace Factory — later known as Hailiya. A century of innovation begins here.","Company"),
    ("index152","2026-03-17","10.5mm Integral Core-Sheath Static Rope","The 10.5mm bonded sheath rope, with its perfect combination of high-strength nylon and polyester fibers, exhibits extremely low elongation and exceptional performance.","Marine"),
    ("index151","2026-03-12","Is Your Lifeline Compromised? What the 2026 Safety Recalls Mean for Your Rope System","Understanding the 2026 safety recall landscape and what it means for rope system selection, inspection, and compliance in professional applications.","Safety"),
    ("index150","2026-03-07","Patent New Product: Huakai Four-Claw Rope — A Safer Cable Pulling Tool","Huakai's patented Four-Claw Rope represents a breakthrough in cable pulling safety, reducing operator risk and improving efficiency in cable installation.","Company"),
    ("index149","2026-02-27","Building Unity Through Collaboration, Securing Safety Through Practice","Jiaolong's cross-departmental training program strengthens team cohesion and technical proficiency across rescue operations, field tactics, and equipment deployment.","Company"),
    ("index148","2026-02-25","Qingdao Huakai (Hailiya Group) Celebrate 2026 Chinese New Year","Singing and Dancing: A Cultural Feast Warmly Concludes the 2026 Chinese New Year Annual Meeting Gala — celebrating another year of milestones.","Company"),
    ("index147","2026-02-06","Comprehensive Analysis of Sailing Rope Systems: From Material Selection to Maintenance","An in-depth guide covering material properties of UHMWPE, Vectran®, and polyester sailing ropes, with selection criteria and care protocols.","Marine"),
    # Page 3
    ("index146","2026-02-02","How Our Fast Rope Delivers High Performance for Tactical and Rescue Operations","High-performance Fast Rope designed for rapid tactical and rescue operations, offering exceptional strength, heat resistance, and controlled grip.","Defence"),
    ("index145","2026-01-23","Major Certification! Hailiya Group's Escape Descent Device Selected for China's National Industrial Safety Catalog","Selected for China's national industrial safety equipment catalog — Hailiya Group's escape descent device, co-developed with Tsinghua University.","Company"),
    ("index144","2026-01-15","Rope Redefined: The Unsung Hero of Every Great Voyage","Modern sailboat rope is a high-tech marvel, engineered from advanced fibers for minimal stretch, lightweight performance, and durability in ocean racing.","Marine"),
    ("index143","2026-01-09","Hailiya Group Rushes to Fire Site to Carry Out Emergency Rescue","Hailiya Group's emergency team quickly responded to a fire at a Qingdao centre, demonstrating professional rescue capability and Jiaolong system effectiveness.","Company"),
    ("index142","2025-12-31","Hailiya Group Celebrate New Year — Happy New Year 2026!","Happy New Year 2026! We look forward to building a stronger future of cooperation — a year of innovation, global expansion, and product excellence.","Company"),
    ("index141","2025-12-01","Delegation from Ceuta Autonomous City Fire Service, Spain, Visits Hailiya Group","The Ceuta Fire Service visited Hailiya Group for an exchange, engaging in in-depth cooperation regarding the 'Jiaolong' rope rescue equipment system.","Company"),
    ("index140","2025-11-27","National Pride! Hailiya Group's 'Jiaolong' Invited as Rope Supplier for GRIMPDAY International Competition","Hailiya's 'Jiaolong' brand selected as official rope supplier for the prestigious GRIMPDAY International Rope Technology Competition.","Company"),
    ("index139","2025-11-24","Competition Rope Supply: Jiaolong Contributes to the 2025 GRIMPDAY CHINA International Competition","From Nov 16–19, 2025 GRIMPDAY CHINA competition took place in Ruyuan, Shaoguan. Hailiya Group's 'Jiaolong' served as official rope supplier.","Company"),
    ("index138","2025-11-20","Pacific Island Nations Climate Change Workshop Delegation Visits Hailiya Group","The Pacific Island Nations Climate Change and Disaster Risk Management Workshop delegation conducted an inspection and exchange visit to Hailiya Group.","Company"),
    ("index137","2025-11-13","10.5mm Sheath-Core Fusion Static Rope — Product Introduction","Introduction to Hailiya's 10.5mm Sheath-Core Fusion Static Rope, featuring advanced bonding technology and EN1891 compliance.","Marine"),
    # Page 4
    ("index136","2025-11-06","Livestock Feeder — Efficient Feeding Solution for Modern Farms","Introducing Hailiya's innovative Livestock Rope product line, providing reliable rope solutions for agricultural and farming applications.","Industry"),
    ("index135","2025-10-30","Hailiya Group's Rope Rescue Equipment Shines at the 21st China International Fire Protection Exhibition","Hailiya Group showcases rope rescue gear at China Fire Expo — Innovation Leads, Global Presence in fire safety and rescue technology.","Company"),
    ("index134","2025-10-23","Royal Thai Embassy Delegation Visits Hailiya Group for Inspection and Exchange","BOI Beijing Chief and Royal Thai Embassy investment delegation visit Hailiya Group in Qingdao for inspection and bilateral cooperation exchange.","Company"),
    ("index133","2025-10-16","JIAOLONG Brand High-Altitude Safety Ropes Integrate Multiple Technologies","JIAOLONG Brand High-Altitude Safety Ropes feature 4 core integrated technologies: EN1891/EN892 compliance, patented core bonding, chemical resistance, and UV stability.","Safety"),
    ("index132","2025-10-10","Anti-Biofouling Marine Ropes — Innovation in Underwater Applications","Hailiya's anti-biofouling marine ropes prevent barnacle and algae growth, extending service life in subsea and mooring applications.","Marine"),
    ("index131","2025-10-09","Spherical Rubber-Sheathed Spiked Cable for Preventing Snagging in Deep-Sea Rock Crevices","Specialized cable design preventing snagging in deep-sea rock crevices — critical for oceanographic research and subsea operations.","Marine"),
    ("index130","2025-09-30","How to Judge the Quality of a Rope?","What makes a high-quality rope? Learn the key parameters: fibre purity, braid consistency, breaking strength testing, and certification compliance.","Industry"),
    ("index129","2025-09-30","Which Ropes Are Recommended for Electric Ascenders?","Electric ascender compatibility depends on rope diameter, sheath thickness, and coefficient of friction. Here is our recommendation guide.","Safety"),
    ("index128","2025-09-30","CCTV-10 'Experiment Site': Dynamic Climbing Rope Energy Conversion Experiment","JIAOLONG Dynamic Climbing Rope featured on national TV programme, demonstrating how energy is absorbed and converted during a climbing fall.","Company"),
    ("index127","2025-09-29","Maintenance and Use of Ropes — Essential Guidelines","Comprehensive guidelines for rope maintenance: storage, washing, inspection intervals, and mandatory retirement criteria for safety ropes.","Industry"),
    # Page 5
    ("index126","2025-09-29","Technical Parameters of Ultra-High Molecular Weight Polyethylene (UHMWPE) Rope","Detailed technical parameters of UHMWPE ropes: molecular weight, tensile strength, elongation, UV resistance, and application guidelines.","Marine"),
    ("index125","2025-09-29","Hailiya Group Hosts 2025 2nd National Water Rescue Comprehensive Skills Open Competition","On September 22, the 2025 2nd National Water Rescue Competition opened in Rizhao City, Shandong Province — Hailiya Group as official host.","Company"),
    ("index124","2025-09-28","Introduction to the Six Exceptional Properties of Aramid III Fiber Ropes","Aramid III fiber ropes offer six key advantages: ultra-high tensile strength, heat resistance, chemical stability, low elongation, aerospace-grade quality.","Marine"),
    ("index123","2025-09-28","What Types of Terminals (Eye Splices) Do Ropes Have?","A complete guide to rope eye splice types: hand-spliced, machine-spliced, heat-bonded, and hardware-terminated loops and thimbles.","Industry"),
    ("index122","2025-09-28","How to Cut Safety Ropes?","The correct cutting method for safety ropes — including heat-sealing, hot knife cutting, and proper end finishing to prevent unravelling.","Safety"),
    ("index121","2025-09-26","Hailiya Group: Small Ropes 'Reaching for the Sky and Ocean'","Hailiya Group's technical evolution and 100+ year history — from traditional rope-making to aerospace and deep-sea application ropes.","Company"),
    ("index120","2025-09-26","From Qingdao, China to Düsseldorf, Germany: Century-Old Hailiya Group Leads Chinese Innovation","At A+A 2023, Century-Old Hailiya Group led 'Chinese Innovation' in rope technology. Returning to A+A 2025 with next-generation products.","Company"),
    ("index119","2025-09-26","Effects of Common Chemical Substances on Safety Ropes for Aerial Work","How do acids, alkalis, solvents, and oils affect rope integrity? A guide to chemical compatibility for aerial work safety ropes.","Safety"),
    ("index118","2025-09-25","Manufacturer of Rappelling Ropes — Qingdao Huakai Ocean Technology","Huakai's rappelling rope range: EN1891 static, EN892 dynamic, and specialty kernmantel ropes for professional rappelling applications.","Marine"),
    ("index117","2025-09-25","Rope Artisans at Qingdao Huakai Ocean: Safeguarding Lives with Mountaineering Ropes","Introduction to mountaineering rope types and functions — from single rope to twin and half rope systems for technical climbing.","Outdoor"),
    # Page 6
    ("index116","2025-09-25","Kevlar Rope Specifications — Applications and Technical Data","Kevlar (Aramid) rope specifications: tensile strength, heat resistance, chemical compatibility, and recommended applications for industrial use.","Marine"),
    ("index115","2025-09-24","Round or Flat: Which is Better for Off-Road Kinetic Recovery Ropes?","Comparing round vs flat kinetic recovery ropes for 4WD off-road use: stretch characteristics, load distribution, and recovery efficiency.","Outdoor"),
    ("index114","2025-09-24","What is the Suitable Length for an Off-Road Kinetic Recovery Rope?","Determining the correct kinetic recovery rope length based on vehicle weight, terrain, and recovery scenario — practical sizing guide.","Outdoor"),
    ("index113","2025-09-24","What Type of Tow Rope (Kinetic Recovery Rope) is Best for Off-Road?","Comprehensive guide to selecting the best kinetic recovery rope for off-road applications: material, elongation, and WLL considerations.","Outdoor"),
    ("index112","2025-09-23","Qingdao Hailiya Group: Mastering the Craft of Ropes for Space and Deep-Sea Missions","From spacecraft deployment ropes to deep-sea exploration cables — Hailiya's precision engineering at the extremes of human endeavour.","Marine"),
    ("index111","2025-09-23","Which Brand of Climbing Rope is Good? Introducing Jiaolong Brand Climbing Rope","A brand comparison guide for climbing ropes — featuring Jiaolong's EN892 and EN1891 certified climbing and rescue ropes.","Outdoor"),
    ("index110","2025-09-23","Do You Really Know Your Rope? 4 Details You Should Know","Four critical rope details often overlooked by professionals: sheath-to-core ratio, elongation under working load, twist angle, and end-fitting compatibility.","Industry"),
    ("index109","2025-09-22","What is Germany's Edelrid Brand Ropes Like? Compare with Jiaolong Ropes","A detailed comparison between German brand Edelrid and Jiaolong ropes across EN certification, performance, and value for professional use.","Industry"),
    ("index108","2025-09-22","What is the American BlueWater Ropes Brand Like? Compare with Jiaolong Ropes","Comparing BlueWater Ropes (USA) with Jiaolong (China) across dynamic and static rope performance, certification, and pricing.","Industry"),
    ("index107","2025-09-22","Manufacturers of High-Performance Fiber Ropes — Global Overview","An overview of the world's leading high-performance fiber rope manufacturers, their specializations, and where Hailiya fits in the global landscape.","Industry"),
    # Page 7
    ("index106","2025-09-20","Research Progress on High-Performance Fiber Braided Ropes for Spacecraft Applications","Technical review of high-performance fiber braided ropes for spacecraft — covering Vectran®, Zylon® PBO, and UHMWPE in space-rated applications.","Marine"),
    ("index105","2025-09-20","Helicopter Fast Rope for Rapid Descent — Design and Specifications","Technical overview of helicopter fast rope design: fibre composition, surface texture, diameter options, and load capacity for military insertion.","Defence"),
    ("index104","2025-09-20","Maintenance and Storage of Ropes — Best Practices Guide","Best practices for professional rope maintenance and storage: UV protection, chemical contamination prevention, and periodic inspection protocols.","Industry"),
    ("index103","2025-09-19","Rope Coatings and Fiber Finishing — Enhancing Performance and Longevity","How rope coatings — polyurethane, silicone, PTFE — affect grip, wear resistance, water repellency, and service life of professional ropes.","Industry"),
    ("index102","2025-09-19","Dyeing Properties of Fiber Ropes — Colour Stability and Safety Coding","Understanding fibre-reactive dyes, colour fastness standards, and the importance of colour coding in rescue and safety rope systems.","Industry"),
    ("index101","2025-09-19","Ultra-High Molecular Weight Polyethylene (UHMWPE) Braided Rope — Complete Overview","Comprehensive introduction to UHMWPE braided rope: molecular structure, manufacturing process, mechanical properties, and comparison with steel wire.","Marine"),
    ("index100","2025-09-18","Correct Usage Methods for Ropes — Professional Guidelines","Professional guidelines for correct rope usage: dynamic loading limits, bending radius, anchor angles, and avoiding common operator errors.","Industry"),
    ("index99","2025-09-18","The Importance of Rope Tensile Testing — Methods and Standards","Why tensile testing matters: ISO, EN, and NFPA test methodologies for rope breaking strength and elongation measurement.","Industry"),
    ("index98","2025-09-18","Geometric Structure of Braided Ropes — Engineering Principles","Exploring the geometry of 8-strand, 12-strand, and 16-strand braided ropes and how construction affects mechanical behaviour.","Industry"),
    ("index97","2025-09-17","Tips for Using Static Ropes — Professional Best Practices","Practical tips for static rope deployment: rigging anchors, load equalisation, edge protection, and descender compatibility for rescue applications.","Safety"),
    # Page 8
    ("index96","2025-09-17","EN892 Standards and Testing for Dynamic Ropes — Complete Guide","What does EN892 testing involve? Fall factor, dynamic elongation, static elongation, impact force, and UIAA fall requirements explained.","Safety"),
    ("index95","2025-09-17","EN1891 Standards and Testing for Static Ropes — Complete Guide","EN1891 type A vs type B static ropes: breaking strength requirements, elongation limits, knotability, and sheath slippage test procedures.","Safety"),
    ("index94","2025-09-16","What Are the Brands of High-Performance Fiber Ropes? 7 Key Brands Reviewed","A review of 7 leading high-performance fiber rope brands including Marlow, Samson, Teufelberger, and where Hailiya's Jiaolong ranks globally.","Industry"),
    ("index93","2025-09-16","Application of Braided Ropes in Spacecraft — Three Primary Scenarios","Three primary spacecraft applications for braided ropes: parachute deployment systems, solar panel deployment, and docking/tethering cables.","Marine"),
    ("index92","2025-09-16","How to Properly Pack a Water Rescue Throwline Bag?","Step-by-step guide to correctly packing a water rescue throwline bag for rapid deployment in swiftwater rescue scenarios.","Safety"),
    ("index91","2025-09-15","Four Major Types of High-Performance Organic Fiber Ropes — Comparison","Comparing Aramid, Polyarylate (Vectran®), Polyimide, and UHMWPE fiber ropes: strength, weight, heat resistance, and cost.","Industry"),
    ("index90","2025-09-15","About High-Performance Fiber Ropes — Introduction and Overview","An accessible introduction to high-performance fiber ropes: what makes them different from conventional ropes and where they excel.","Industry"),
    ("index89","2025-09-15","Creep and Relaxation Behavior of Braided Ropes — Engineering Analysis","Engineering analysis of rope creep and relaxation: how UHMWPE, Vectran®, and Aramid fibers behave differently under sustained load.","Industry"),
    ("index88","2025-09-13","How Many Tons and How Long Should an Off-Road Kinetic Recovery Rope Be?","Sizing guide for off-road kinetic recovery ropes: recommended breaking strength and length relative to vehicle gross weight.","Outdoor"),
    ("index87","2025-09-13","Tow Ropes for Off-Road Vehicles — Selection and Safety Guide","How to select the right tow rope for off-road use: the difference between static tow ropes and kinetic recovery ropes.","Outdoor"),
    # Page 9
    ("index86","2025-09-13","What Are the Different Types of Ropes? — Complete Classification Guide","A complete classification of rope types by construction (braided, twisted, kernmantel), material (nylon, polyester, UHMWPE), and application.","Industry"),
    ("index85","2025-09-12","The Ultimate Guide to Climbing Ropes: Everything You Need to Know in One Article","Comprehensive guide to climbing ropes: dynamic vs static, single vs twin vs half rope, diameter selection, and fall rating interpretation.","Outdoor"),
    ("index84","2025-09-12","World Renowned Climbing Rope Brands — Quality Comparison","A global comparison of climbing rope brands including Jiaolong, Petzl, Mammut, and Sterling — quality, certification, and value analysis.","Outdoor"),
    ("index83","2025-09-12","Static Ropes — From Fiber to Rope: Raw Materials and Manufacturing","From raw nylon fiber to finished EN1891 static rope: the complete manufacturing process explained with material properties at each stage.","Safety"),
    ("index82","2025-09-11","Differences Between Static Ropes and Safety Ropes — Clear Explanation","Clarifying the often-confused distinction between static (EN1891) ropes, dynamic (EN892) ropes, and general-purpose safety ropes.","Safety"),
    ("index81","2025-09-11","UIAA Rope Standards of the International Climbing and Mountaineering Federation","UIAA (International Climbing and Mountaineering Federation) rope standards: what UIAA-certified means and how it compares to EN standards.","Industry"),
    ("index80","2025-09-11","Qingdao Huakai Ocean Science and Technology to Showcase Innovative Safety Solutions at A+A 2025 in Düsseldorf","Huakai to feature Jiaolong safety solutions at A+A 2025 in Düsseldorf — Europe's leading occupational safety and health trade fair.","Company"),
    ("index79","2025-09-10","The Century-Long History of Qingdao Hailiya Group","The complete century-long history of Qingdao Hailiya Group — from the 1923 Xiecheng Lace Factory to today's global rope technology leader.","Company"),
    ("index78","2025-09-10","Types of Climbing Ropes: Dynamic Ropes and Static Ropes — Explained","Climbing ropes are divided into dynamic ropes and static ropes. Differences, characteristics, and when to use each type explained clearly.","Outdoor"),
    ("index77","2025-09-10","Power Traction Ropes Made from UHMWPE — Applications in Power Transmission","UHMWPE power traction ropes replacing traditional steel wire ropes in electricity grid tower maintenance and transmission line pulling.","Marine"),
    # Page 10
    ("index76","2025-09-09","Rock Climbing Rope Manufacturer — Qingdao Huakai Ocean Technology","Introduction to Qingdao Huakai as a rock climbing rope manufacturer, including our climbing rope product range and manufacturing advantages.","Outdoor"),
    ("index75","2025-09-09","Fast Rope Performance: Can Rope Damage Affect Fast Rope Performance?","Analysis of how rope damage — surface abrasion, core damage, heat exposure — affects fast rope performance during helicopter insertion.","Defence"),
    ("index74","2025-09-08","Safety Regulations for High-Altitude Rescue Ropes — Standards Overview","Overview of safety regulations governing high-altitude rescue ropes: EN1891, NFPA 1983, UIAA, and Chinese GB standards compared.","Safety"),
    ("index73","2025-09-08","What are the EU CE Certification Standards for Static Ropes Complying with EN 1891?","Detailed breakdown of EU CE certification requirements for static ropes under EN 1891, including type A vs type B distinctions.","Safety"),
    ("index72","2025-09-08","Which Accessory Cord is Suitable for a Prusik Hitch?","The correct accessory cord (EN564) diameter and material for prusik hitches — safety considerations for rappelling and ascending systems.","Safety"),
    ("index71","2025-09-08","Correct Usage of Safety Ropes — Professional Guidelines","Step-by-step guide to correct safety rope usage in height work, including anchor setup, load management, and inspection before use.","Safety"),
    ("index70","2025-09-06","Three Major Advantages of Jiaolong Brand Buoy Ropes","Three key advantages of Jiaolong buoy ropes over conventional ropes: corrosion resistance, UV stability, and certified breaking strength.","Marine"),
    ("index69","2025-09-06","Hailiya Marine Special Ropes Achieve Four 'China Firsts'","Hailiya Marine Special Ropes break four national records in China: tensile strength, depth rating, UV resistance, and elongation control.","Company"),
    ("index68","2025-09-06","A Type of High-Strength Low-Elongation Static Rope","Introduction to Jiaolong's high-strength low-elongation static rope series, combining nylon core with polyester sheath for superior rescue performance.","Safety"),
    ("index67","2025-09-05","Rope Standards and Certification: EN and CE Certification Explained","A complete guide to EN and CE rope certification: what each standard covers, how testing works, and why certification matters for safety.","Industry"),
    # Page 11
    ("index66","2025-09-05","Buoy Rope: The Innovative Link in the Ocean Depths","How buoy ropes connect surface monitoring systems to deep-sea anchors — the engineering challenge of strength, flexibility, and corrosion resistance.","Marine"),
    ("index65","2025-09-05","Characteristics of Nylon Buoy Ropes — Properties and Applications","Nylon buoy rope characteristics: 26–36% elongation at break, seawater resistance, UV durability, and applications in scientific research.","Marine"),
    ("index64","2025-09-04","Difference Between Single Rope Technique (SRT) and Double Rope Technique (DRT)","Explaining the key differences between SRT and DRT rope access techniques — when each is used and their respective safety implications.","Safety"),
    ("index63","2025-09-04","What is Rope Creep? — Understanding Long-Term Deformation","Rope creep explained: how UHMWPE and Vectran® behave differently under long-term sustained loads and how to account for it in system design.","Industry"),
    ("index62","2025-09-04","Choose Type A or Type B Static Rope? Here is the Answer!","Type A vs Type B static ropes under EN1891: the differences in strength, elongation limits, and appropriate applications for each type.","Safety"),
    ("index61","2025-09-04","What Types of Rope Terminations (Eyes) Are There? Common Types Introduced","Common rope termination types: hand-spliced eye, machine-spliced eye, thimble eye, and hardware-terminated loops — when to use each.","Industry"),
    ("index60","2025-09-02","Differences Between UHMWPE Ropes and Aramid Ropes — How to Choose","A detailed comparison of UHMWPE and Aramid ropes: strength-to-weight ratio, UV resistance, heat resistance, and application suitability.","Marine"),
    ("index59","2025-09-02","High-Performance Ship Mooring Ropes — Specifications and Selection Guide","Guide to selecting high-performance ship mooring ropes: UHMWPE vs polyamide vs polyester for different vessel types and port conditions.","Marine"),
    ("index58","2025-09-02","What is the Fall Factor? Understanding the Physics of Climbing Safety","The fall factor in climbing: how it's calculated, why it matters more than fall distance, and how it affects dynamic rope choice.","Outdoor"),
    ("index57","2025-09-02","Characteristics of Ultra-High Molecular Weight Polyethylene Sailing Rope","UHMWPE sailing rope: minimal stretch, high strength, UV and seawater resistance — the optimal choice for racing and offshore sailing.","Marine"),
    # Page 12
    ("index56","2025-09-01","Correct Use and Maintenance of Soft Shackles — Tips for Safe Operation","How to correctly use and maintain synthetic soft shackles: inspection, breaking strength limitations, and replacing worn units safely.","Outdoor"),
    ("index55","2025-09-01","Pros and Cons of Soft Shackles vs Steel Shackles — Complete Comparison","Comprehensive comparison: soft shackles (UHMWPE) vs traditional steel shackles — weight, strength, safety on failure, corrosion, and cost.","Outdoor"),
    ("index54","2025-09-01","How to Choose the Diameter and Length of an Off-Road Kinetic Recovery Rope?","Sizing guide for kinetic recovery ropes: diameter vs vehicle weight tables, recommended lengths, and how to account for stretch in recovery.","Outdoor"),
    ("index53","2025-08-29","How Off-Road Kinetic Recovery Ropes Work — Science and Mechanics","The basic principles and science behind kinetic energy recovery ropes: elastic storage, energy release, and why they outperform rigid tow straps.","Outdoor"),
    ("index52","2025-08-29","What are the Main Materials Used for Safety Ropes?","Overview of safety rope materials: nylon, polyester, UHMWPE, and Aramid — properties, trade-offs, and matching material to application.","Safety"),
    ("index51","2025-08-29","How to Choose a Cost-Effective Rope? Value Selection Guide","How to evaluate rope cost-effectiveness: balancing certified performance, service life, and total cost of ownership for professional buyers.","Industry"),
    ("index50","2025-08-28","What is the Difference Between Jiaolong Static Rope and Low Stretch Kernmantle Rope?","Clarifying the difference between Jiaolong's standard static rope and their low-stretch kernmantle rope — construction, elongation, and use case.","Safety"),
    ("index49","2023-08-23","Outdoor Retailer Summer Market 2023 — Hailiya Group Participates","Hailiya Group's participation in Outdoor Retailer Summer Market 2023 — showcasing Jiaolong climbing and outdoor rope systems to global buyers.","Company"),
    ("index48","2022-08-12","New Website of Qingdao Huakai Rope Is Online Now","New window, new face to the world — Qingdao Huakai Ocean Science and Technology launches its new official website for global customers.","Company"),
]

# ── Category → colour mapping ──────────────────────────────────────────────────
CAT_COLOURS = {
    "Safety":   "#d35400",
    "Marine":   "#1565c0",
    "Defence":  "#4a235a",
    "Outdoor":  "#1b5e20",
    "Company":  "#c8a84b",
    "Industry": "#0d2137",
}

# ── Category → local image fallback ───────────────────────────────────────────
CAT_IMAGES = {
    "Safety":   "images/3071e50616036b30590663c384f49b3b.png",
    "Marine":   "images/890a7756195138154e0eb2390ab9e7a8.jpg",
    "Defence":  "images/e1a9acdd4c034e862bf8177aa4d527f5.png",
    "Outdoor":  "images/prod_sailing_1.jpg",
    "Company":  "images/workshop_exterior.png",
    "Industry": "images/prod_uhmwpe_1.jpg",
}

# ── Pre-known article images (from earlier fetches) ───────────────────────────
KNOWN_IMAGES = {
    "index167": "https://www.hailiya.com.au/upload/default/20260514/65c7421e1afe7d388ee4d36879ed7c68.jpg",
    "index159": "https://www.hailiya.com.au/upload/default/20260414/0fa811b869dbfd56d8b9b3a43efdccf1.jpg",
    "index161": "https://www.hailiya.com.au/upload/default/20260421/a05a6960809ff6118b9da2feda6a4a8d.jpg",
}

# ── Download article thumbnail images ─────────────────────────────────────────
def fetch_article_image(article_id):
    """Fetch article page and extract first <img> in content area."""
    if article_id in KNOWN_IMAGES:
        return KNOWN_IMAGES[article_id]
    url = f"{BASE_URL}/news/{article_id}.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read().decode('utf-8', errors='replace')
        # Look for upload images in content
        imgs = re.findall(r'src=["\']([^"\']*upload/default[^"\']+)["\']', body)
        if imgs:
            return "https://www.hailiya.com.au" + imgs[0] if imgs[0].startswith('/') else imgs[0]
    except:
        pass
    return None

def download_image(url, fname):
    """Download image to images/ folder. Returns local path or None."""
    dest = os.path.join(IMG_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 2000:
        return "images/" + fname
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":BASE_URL})
        with urllib.request.urlopen(req, timeout=20) as r, open(dest, 'wb') as f:
            f.write(r.read())
        if os.path.getsize(dest) > 2000:
            print(f"  DL  {fname}")
            return "images/" + fname
        else:
            os.remove(dest)
    except Exception as e:
        pass
    return None

# Download images for all articles
print("=== Downloading article images ===")
article_images = {}  # article_id -> local_path or cat_fallback

for idx, (art_id, date, title, excerpt, cat) in enumerate(ALL_ARTICLES):
    fname = f"news_{art_id}.jpg"
    dest  = os.path.join(IMG_DIR, fname)
    local_path = None

    # Use pre-known images first
    if art_id in KNOWN_IMAGES:
        local_path = download_image(KNOWN_IMAGES[art_id], fname)

    if not local_path:
        # Try fetching article page to find image
        img_url = fetch_article_image(art_id)
        if img_url:
            local_path = download_image(img_url, fname)

    if local_path:
        article_images[art_id] = local_path
        print(f"  OK  {art_id} — {fname}")
    else:
        article_images[art_id] = CAT_IMAGES[cat]
        print(f"  FB  {art_id} — fallback ({cat})")

    # Be polite to server
    if idx % 5 == 4:
        time.sleep(0.5)

print(f"\nImages ready: {sum(1 for v in article_images.values() if v.startswith('images/news_'))} downloaded, "
      f"{sum(1 for v in article_images.values() if not v.startswith('images/news_'))} fallback")

# ── Build news HTML ────────────────────────────────────────────────────────────
PER_PAGE = 10
TOTAL    = len(ALL_ARTICLES)
N_PAGES  = (TOTAL + PER_PAGE - 1) // PER_PAGE

def esc(s):
    return html_module.escape(str(s))

def cat_badge(cat):
    colour = CAT_COLOURS.get(cat, "#333")
    return f'<span class="na-cat" style="background:{colour};">{esc(cat)}</span>'

def format_date(d):
    """2026-05-14 → 14 May 2026"""
    parts = d.split('-')
    months = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    try:
        return f"{int(parts[2])} {months[int(parts[1])]} {parts[0]}"
    except:
        return d

# Build all article cards
ARTICLE_CARDS = []
for art_id, date, title, excerpt, cat in ALL_ARTICLES:
    img = article_images.get(art_id, CAT_IMAGES[cat])
    is_transparent = img.endswith('.png') or img.endswith('.svg')
    img_style = 'object-fit:contain;background:#f0f4f8;' if is_transparent else 'object-fit:cover;'
    ARTICLE_CARDS.append(f'''        <div class="na-card" data-cat="{esc(cat)}">
          <div class="na-img-wrap">
            <img src="{esc(img)}" alt="{esc(title)}" style="{img_style}">
          </div>
          <div class="na-content">
            <div class="na-meta">{cat_badge(cat)}<span class="na-date">{format_date(date)}</span></div>
            <div class="na-title">{esc(title)}</div>
            <div class="na-excerpt">{esc(excerpt)}</div>
          </div>
        </div>''')

# Build page groups
PAGE_GROUPS = []
for p in range(N_PAGES):
    cards = ARTICLE_CARDS[p*PER_PAGE:(p+1)*PER_PAGE]
    PAGE_GROUPS.append(f'      <div class="na-page" id="na-page-{p+1}" style="display:{"block" if p==0 else "none"};">\n' +
                        '\n'.join(cards) + '\n      </div>')

# Build pagination buttons
PAGINATION = '      <div class="na-pagination">\n'
PAGINATION += '        <button class="na-pager" id="na-prev" onclick="naPage(-1)" disabled>&#8592; Prev</button>\n'
for p in range(N_PAGES):
    active = ' na-pager--active' if p==0 else ''
    PAGINATION += f'        <button class="na-pager na-pager--num{active}" onclick="naGoPage({p+1})">{p+1}</button>\n'
PAGINATION += '        <button class="na-pager" id="na-next" onclick="naPage(1)">Next &#8594;</button>\n'
PAGINATION += '      </div>\n'

# Build category filter
CATEGORIES = ["All","Safety","Marine","Defence","Outdoor","Company","Industry"]
FILTER_HTML = '      <div class="na-filters">\n'
for c in CATEGORIES:
    active = ' na-filter--active' if c == "All" else ''
    FILTER_HTML += f'        <button class="na-filter{active}" onclick="naFilter(\'{c}\')">{c}</button>\n'
FILTER_HTML += '      </div>\n'

NEW_NEWS_SECTION = f'''
  <!-- ===================== NEWS ===================== -->
  <section class="section" id="news">
    <div class="container">
      <div class="section-header fade-in">
        <span class="section-label">Latest News</span>
        <div class="divider"></div>
        <h2 class="section-title">News &amp; Updates</h2>
        <p class="section-subtitle">All {TOTAL} articles from Huakai &amp; Jiaolong — industry knowledge, company news, product updates, and technical insights.</p>
      </div>
{FILTER_HTML}
      <div id="na-container">
{chr(10).join(PAGE_GROUPS)}
      </div>
{PAGINATION}    </div>
  </section>

'''

# ── News CSS ──────────────────────────────────────────────────────────────────
NEWS_CSS = '''
    /* ── News Archive ──────────────────────────────── */
    .na-filters { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:28px; }
    .na-filter {
      padding:7px 18px; border:2px solid var(--border); border-radius:100px;
      font-size:13px; font-weight:600; background:var(--white); color:var(--text-light);
      cursor:pointer; transition:var(--transition);
    }
    .na-filter:hover, .na-filter--active {
      border-color:var(--blue); background:var(--blue); color:#fff;
    }
    .na-card {
      display:flex; gap:20px; padding:22px 0; border-bottom:1px solid var(--border);
      align-items:flex-start; cursor:default;
    }
    .na-card:last-child { border-bottom:none; }
    .na-img-wrap {
      flex-shrink:0; width:200px; height:134px; border-radius:10px;
      overflow:hidden; background:#f0f4f8;
    }
    .na-img-wrap img { width:100%; height:100%; transition:transform 0.35s; }
    .na-card:hover .na-img-wrap img { transform:scale(1.05); }
    .na-content { flex:1; min-width:0; }
    .na-meta { display:flex; align-items:center; gap:10px; margin-bottom:9px; }
    .na-cat {
      font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;
      color:#fff; border-radius:4px; padding:3px 8px;
    }
    .na-date { font-size:12px; color:var(--mid-gray); }
    .na-title { font-size:17px; font-weight:700; color:var(--navy); line-height:1.4; margin-bottom:8px; }
    .na-excerpt { font-size:13px; color:var(--text-light); line-height:1.7; }

    /* Pagination */
    .na-pagination { display:flex; justify-content:center; gap:6px; padding:32px 0 8px; flex-wrap:wrap; }
    .na-pager {
      padding:8px 14px; border:2px solid var(--border); border-radius:8px;
      font-size:13px; font-weight:600; background:var(--white); color:var(--navy);
      cursor:pointer; transition:var(--transition); min-width:40px;
    }
    .na-pager:hover:not(:disabled) { border-color:var(--blue); color:var(--blue); }
    .na-pager--active { background:var(--navy); color:#fff; border-color:var(--navy); }
    .na-pager:disabled { opacity:0.4; cursor:not-allowed; }

    @media (max-width:680px) {
      .na-card { flex-direction:column; }
      .na-img-wrap { width:100%; height:180px; }
    }
'''

NEWS_JS = f'''
  // ── News pagination & filter ────────────────────────────
  var _naPage = 1, _naTotalPages = {N_PAGES}, _naFilter = 'All';
  var _naAllData = {json.dumps([(a[0],a[2],a[1],a[3],a[4]) for a in ALL_ARTICLES])};

  function naRender() {{
    var filtered = _naFilter === 'All' ? _naAllData : _naAllData.filter(function(a){{ return a[4]===_naFilter; }});
    var perPage = 10;
    var totalPages = Math.max(1, Math.ceil(filtered.length / perPage));
    _naPage = Math.min(_naPage, totalPages);
    var start = (_naPage-1)*perPage, end = start+perPage;
    var slice = filtered.slice(start, end);

    var catColours = {json.dumps(CAT_COLOURS)};
    var catImgs    = {json.dumps(CAT_IMAGES)};
    var artImgs    = {json.dumps(article_images)};

    var html = '';
    slice.forEach(function(a) {{
      var id=a[0], title=a[1], date=a[2], excerpt=a[3], cat=a[4];
      var img = artImgs[id] || catImgs[cat] || '';
      var cc  = catColours[cat] || '#333';
      var isPng = img.endsWith('.png')||img.endsWith('.svg');
      var imgStyle = isPng ? 'object-fit:contain;background:#f0f4f8;' : 'object-fit:cover;';
      html += '<div class="na-card">' +
        '<div class="na-img-wrap"><img src="'+img+'" alt="" style="'+imgStyle+'" loading="lazy"></div>' +
        '<div class="na-content">' +
          '<div class="na-meta"><span class="na-cat" style="background:'+cc+';">'+cat+'</span>' +
            '<span class="na-date">'+date+'</span></div>' +
          '<div class="na-title">'+title+'</div>' +
          '<div class="na-excerpt">'+excerpt+'</div>' +
        '</div></div>';
    }});
    document.getElementById('na-container').innerHTML = html || '<p style="padding:40px 0;color:var(--mid-gray);">No articles in this category.</p>';

    // Pagination
    var pages = '';
    for (var p=1; p<=totalPages; p++) {{
      pages += '<button class="na-pager na-pager--num'+(p===_naPage?' na-pager--active':'')+'" onclick="naGoPage('+p+')">'+p+'</button>';
    }}
    var pager = document.querySelector('.na-pagination');
    if (pager) {{
      pager.innerHTML =
        '<button class="na-pager" onclick="naPage(-1)" '+((_naPage<=1)?'disabled':'')+'>&#8592; Prev</button>' +
        pages +
        '<button class="na-pager" onclick="naPage(1)" '+((_naPage>=totalPages)?'disabled':'')+'>Next &#8594;</button>';
    }}
  }}

  function naPage(dir) {{ _naPage = Math.max(1, _naPage+dir); naRender(); window.scrollTo({{top:document.getElementById('news').offsetTop-80,behavior:'smooth'}}); }}
  function naGoPage(p) {{ _naPage=p; naRender(); window.scrollTo({{top:document.getElementById('news').offsetTop-80,behavior:'smooth'}}); }}
  function naFilter(cat) {{
    _naFilter=cat; _naPage=1; naRender();
    document.querySelectorAll('.na-filter').forEach(function(b){{b.classList.toggle('na-filter--active', b.textContent===cat);}});
  }}

  // Init
  naRender();
'''

# ── Read and patch index.html ──────────────────────────────────────────────────
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add news CSS before </style>
if '/* ── News Archive' not in html:
    html = html.replace('  </style>', NEWS_CSS + '  </style>', 1)
    print("OK   Add news archive CSS")
else:
    print("SKIP news CSS (already present)")

# 2. Replace entire news section
# Find section boundaries
ns = html.find('\n  <!-- ===================== NEWS ===================== -->')
ne = html.find('\n\n  <!-- ===================== AWARDS')
if ns != -1 and ne != -1:
    html = html[:ns] + NEW_NEWS_SECTION + html[ne:]
    print(f"OK   Replace news section ({TOTAL} articles, {N_PAGES} pages)")
else:
    print(f"MISS news section (start={ns}, end={ne})")

# 3. Add news JS before </script> closing (inject into the last <script> block)
news_js_anchor = '\n})();\n</script>'
if '// ── News pagination' not in html:
    if news_js_anchor in html:
        html = html.replace(news_js_anchor, '\n' + NEWS_JS + '\n})();\n</script>', 1)
        print("OK   Add news pagination JS")
    else:
        # Fallback: append before closing </body>
        html = html.replace('</body>', f'\n<script>\n{NEWS_JS}\n</script>\n</body>', 1)
        print("OK   Add news JS (appended before </body>)")
else:
    print("SKIP news JS (already present)")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone. File: {len(html.encode('utf-8')):,} bytes | Articles: {TOTAL} | Pages: {N_PAGES}")
