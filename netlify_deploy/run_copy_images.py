import shutil, os

BASE = r"C:\Users\vedan\Desktop\Haili\netlify_deploy"
SRC  = os.path.join(BASE, "Unzipped Hailiya Rope Photos")
DEST = os.path.join(BASE, "images", "products")

copies = [
    # Marine
    (r"UHMWPE Ropes\UHMWPE Rope\UHMWPE1-1.jpg",                                                   "uhmwpe-12strand.jpg"),
    (r"Synthetice Grips\Synthetic Grips\grip.jpg",                                                  "synthetic-grips.jpg"),
    (r"Sailing Ropes\sailing rope\Sailing Rope.jpg",                                                "sailboat-rope.jpg"),
    (r"Recovery Ropes\Recovery Rope\拖车绳-800-1.jpg",                                              "tow-rope-marine.jpg"),
    # Defence
    (r"UHMWPE Ropes\UHMWPE Rope\UHMWPE1.jpg",                                                      "uhmwpe-defence.jpg"),
    (r"Dynamic Ropes\Dynamic Rope\主图\1A4A9600_副本.png",                                          "fast-rope.png"),
    (r"Dynamic Ropes\Dynamic Rope\climbing Rope-8.jpg",                                             "combat-training.jpg"),
    (r"Recovery Ropes\Recovery Rope\Qingdao-Huakai-Ocean-Science-and-Technology-Co-Ltd- (1).jpg",  "ship-towing.jpg"),
    # Safety
    (r"Static Ropes\Static Rope\静力绳主图\主图 (1).jpg",                                           "static-rope-en1891.jpg"),
    (r"Dynamic Ropes\Dynamic Rope\主图\3.jpg",                                                      "dynamic-rope-en892.jpg"),
    (r"Accessory Cord\Accessory Cord\6mm辅绳原图_副本.png",                                        "accessory-cord.png"),
    (r"Water Rescue Ropes\Water Rescue Rope\Floating Rescue Rope\DSC_4834.jpg",                    "throwline.jpg"),
    (r"Static Ropes\Static Rope\High-Rise-Window-Cleaning-in-Denver-Colorado2-960x634.jpg",        "canyoning-rope.jpg"),
    (r"Synthetice Grips\Synthetic Grips\LIFTING ROPE.jpg",                                         "lanyard.jpg"),
    (r"Synthetice Grips\Synthetic Grips\InkedLIFTING ROPE2_LI.jpg",                               "webbing.jpg"),
    # Outdoor
    (r"Dynamic Ropes\Dynamic Rope\主图\6.jpg",                                                      "od-dynamic.jpg"),
    (r"Static Ropes\Static Rope\Static Rope-1.jpg",                                                 "od-static.jpg"),
    (r"Recovery Ropes\Recovery Rope\recovery rope.jpg",                                             "od-kinetic.jpg"),
]

for rel_src, dest_name in copies:
    src_path  = os.path.join(SRC, rel_src)
    dest_path = os.path.join(DEST, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"OK  {dest_name}")
    else:
        print(f"MISSING  {rel_src}")
