#!/usr/bin/env python3
"""Build the full GT Accuracy catalog page from scraped product data."""
import os
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

SHOP_DIR = "assets/images/shop"
os.makedirs(SHOP_DIR, exist_ok=True)

# (name, brand, price, image_url_or_None, product_url, category, sub)
# image_url_or_None: None means use the NEW GT logo placeholder card
PRODUCTS = [
    # ── RIFLES ────────────────────────────────────────────────
    ("GTA CoyDog – 6mm BR", "GT Accuracy", "$4,399.99", None,
     "https://gtaccuracy.com/product/gta-coydog-6mm-br/", "Rifles", "GTA Custom"),
    ("GTA CoyDog – 6mm Creedmoor", "GT Accuracy", "$4,399.99", None,
     "https://gtaccuracy.com/product/gta-coydog-6mm-creedmoor/", "Rifles", "GTA Custom"),
    ("GTA CoyDog – 6mm Dasher", "GT Accuracy", "$4,399.99", None,
     "https://gtaccuracy.com/product/gta-coydog-6mm-dasher/", "Rifles", "GTA Custom"),
    ("GTA CoyDog – Build Your Own", "GT Accuracy", "Configure", None,
     "https://gtaccuracy.com/product/gta-coydog-rifle/", "Rifles", "GTA Custom"),
    ("GTA F-Open – Kestros", "GT Accuracy", "$7,200", None,
     "https://gtaccuracy.com/product/gta-f-open-rifle-kestros/", "Rifles", "GTA Custom"),
    ("GTA F-Open – Lowrider XL BumbleBee", "GT Accuracy", "$8,700", None,
     "https://gtaccuracy.com/product/gta-f-open-rifle-lowrider-xl-bumblebee/", "Rifles", "GTA Custom"),
    ("Ruger American Gen II Predator – 22 ARC", "Ruger", "$635",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/Predator_Gen2_2.jpg",
     "https://gtaccuracy.com/product/ruger-american-rifle-generation-ii-predator-22-arc/", "Rifles", "Production"),
    ("Ruger American Gen II Predator – 243 Win", "Ruger", "$635",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/Predator_Gen2_2.jpg",
     "https://gtaccuracy.com/product/ruger-american-rifle-generation-ii-predator-243-win/", "Rifles", "Production"),
    ("Ruger American Gen II Predator – 6mm ARC", "Ruger", "$635",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/Predator_Gen2_2.jpg",
     "https://gtaccuracy.com/product/ruger-american-rifle-generation-ii-predator-6mm-arc/", "Rifles", "Production"),
    ("Ruger American Gen II Predator – 6mm Creedmoor", "Ruger", "$635",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/Predator_Gen2_2.jpg",
     "https://gtaccuracy.com/product/ruger-american-rifle-generation-ii-predator-6mm-creedmoor/", "Rifles", "Production"),

    # ── BARRELS ───────────────────────────────────────────────
    ('Bartlein Barrel: 6mm – 13.5T – 28" – HV', "Bartlein", "$425", None,
     "https://gtaccuracy.com/product/bartlein-barrel-6mm-13-5t-28-hv/", "Barrels", "Blanks"),
    ('Bartlein Barrel: 6mm – 14T – 32" – STR', "Bartlein", "$495", None,
     "https://gtaccuracy.com/product/bartlein-barrel-6mm-14t-32-str/", "Barrels", "Blanks"),
    ('Bartlein Barrel: 7mm – 8.5T – 32" – HV', "Bartlein", "$495", None,
     "https://gtaccuracy.com/product/bartlein-barrel-7mm-8-5t-32-hv/", "Barrels", "Blanks"),
    ('Brux Barrel: 22 Cal – 8T – 28" – RVC', "Brux", "$465", None,
     "https://gtaccuracy.com/product/brux-barrel-22-cal-8t-28-rvc/", "Barrels", "Blanks"),
    ('Brux Barrel: 25 Cal – 7.5T – 28" – MTU', "Brux", "$475", None,
     "https://gtaccuracy.com/product/brux-barrel-25cal-7-5t-28-mtu/", "Barrels", "Blanks"),
    ('Brux Barrel: 6mm – 7.83T – 28" – HV', "Brux", "$465", None,
     "https://gtaccuracy.com/product/brux-barrel-6mm-7-83t-28-hv/", "Barrels", "Blanks"),
    ('Brux Barrel: 6mm – 7.83T – 30" – HV', "Brux", "$450", None,
     "https://gtaccuracy.com/product/brux-barrel-6mm-7-83t-30-hv/", "Barrels", "Blanks"),
    ('Brux Barrel: 6mm – 7.83T – 30" – STR', "Brux", "$475", None,
     "https://gtaccuracy.com/product/brux-barrel-6mm-7-83t-30-str/", "Barrels", "Blanks"),
    ('Brux Barrel: 7mm – 8.5T – 32" – STR', "Brux", "$475", None,
     "https://gtaccuracy.com/product/brux-barrel-7mm-8-5t-32-str/", "Barrels", "Blanks"),
    ('Brux 6mm Dasher Prefit – Borden MXD/BKXD', "Brux", "$1,200", None,
     "https://gtaccuracy.com/product/brux-borden-mxd-bkxd-6mm-dasher-prefit-268-neck-135-fb/", "Barrels", "Prefit"),
    ('Brux 308 Win FTR Prefit – w/ EC V2 Tuner', "Brux", "$1,150", None,
     "https://gtaccuracy.com/product/brux-308-win-prefit-342-neck-10-twist-with-ec-v2ss-tuner-borden-bktr/", "Barrels", "Prefit"),
    ('Brux 7-6.5 PRCW Prefit .316 Neck', "Brux", "$1,150", None,
     "https://gtaccuracy.com/product/brux-7-6-5-prcw-prefit-316-neck-8-5-twist-with-ec-v2-tuner-borden-brmxd-bkxd-copy/", "Barrels", "Prefit"),
    ('Brux 7-6.5 PRCW Prefit .319 Neck', "Brux", "$1,150", None,
     "https://gtaccuracy.com/product/brux-7-6-5-prcw-319-neck-barrel-with-ec-v2-tuner/", "Barrels", "Prefit"),
    ('Krieger Barrel: 6mm – 10T – 32" – STR', "Krieger", "$525",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/KreigerBarrels.png",
     "https://gtaccuracy.com/product/krieger-barrel-6mm-10t-32-str/", "Barrels", "Blanks"),
    ("OMR Carbon Fiber 22 Cal Barrel", "OMR", "$800",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/OMR_Blank.jpg",
     "https://gtaccuracy.com/product/omr-carbon-fiber-22-cal-barrel/", "Barrels", "Blanks"),
    ("OMR Carbon Fiber 6mm Barrel", "OMR", "$800",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/OMR_Blank.jpg",
     "https://gtaccuracy.com/product/omr-carbon-fiber-6mm-barrel/", "Barrels", "Blanks"),
    ("Proof Research 22 Cal Barrel", "Proof Research", "$899",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/PR_6mm.jpg",
     "https://gtaccuracy.com/product/proof-research-22-cal-barrel/", "Barrels", "Blanks"),

    # ── RECEIVERS / ACTIONS ───────────────────────────────────
    ("Borden Black Knight Receiver – 308", "Borden", "$2,200",
     "https://gtaccuracy.com/wp-content/uploads/2025/06/B-RLR-LS.webp",
     "https://gtaccuracy.com/product/borden-black-knight-receiver-right-bolt-left-port-right-eject-308-bolt-face/", "Receivers", "Actions"),
    ("Borden Black Knight XD – RB/LP/RE 308", "Borden", "$2,400",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/BKXD.jpg",
     "https://gtaccuracy.com/product/borden-black-knight-xd-receiver-right-bolt-left-port-right-eject-308-bolt-face/", "Receivers", "Actions"),
    ("Borden Black Knight XD – RB/RP 308", "Borden", "$2,400",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/BKXD.jpg",
     "https://gtaccuracy.com/product/borden-black-knight-xd-receiver-right-bolt-right-port-308-bolt-face/", "Receivers", "Actions"),
    ("Borden Black Knight XD – RB/RP Mag", "Borden", "$2,400",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/BKXD.jpg",
     "https://gtaccuracy.com/product/borden-black-knight-xd-receiver-right-bolt-right-port-mag-bolt-face/", "Receivers", "Actions"),
    ("Borden BRM Receiver – RB/LP/BE 308", "Borden", "$1,820", None,
     "https://gtaccuracy.com/product/borden-brm-receiver-right-bolt-left-port-bottom-eject-single-shot-308-bolt-face-ground-finish/", "Receivers", "Actions"),
    ("Borden BRMXD – RB/LP/BE 308", "Borden", "$2,050",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/IMG_8426.jpeg",
     "https://gtaccuracy.com/product/borden-brmxd-receiver-right-bolt-left-port-bottom-eject-single-shot-308-bolt-face-ground-finish/", "Receivers", "Actions"),
    ("Borden BRMXD – RB/LP/RE 308", "Borden", "$1,875",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/MXD-RBLPRE-e1736023420534.jpg",
     "https://gtaccuracy.com/product/borden-brmxd-receiver-right-bolt-left-port-right-eject-single-shot-308-bolt-face-ground-finish/", "Receivers", "Actions"),
    ("Borden Mountaineer IL RR SA – 308", "Borden", "$1,950",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden_MountaineerRR.jpg",
     "https://gtaccuracy.com/product/borden-mountaineer-il-rr-sa-receiver-right-bolt-right-port-single-shot-308-bolt-face-ground-finish/", "Receivers", "Actions"),
    ("Borden Mountaineer IL SA LH – 308", "Borden", "$1,469.99",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden_MountaineerRR.jpg",
     "https://gtaccuracy.com/product/borden-mountaineer-il-sa-receiver-left-hand-repeater-308-bolt-face-wyatt-short-mag-wellintegral-lug-standard-handle-bead-blast-finish/", "Receivers", "Actions"),
    ("Borden Mountaineer IL SA RH – Nitride", "Borden", "$1,700",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/IMG_8418.jpeg",
     "https://gtaccuracy.com/product/borden-mountaineer-il-sa-receiver-right-hand-repeater-308-bolt-face-wyatt-short-mag-well-nitride/", "Receivers", "Actions"),
    ("Borden Timberline – Mag", "Borden", "$1,500",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden_Timberline.jpg",
     "https://gtaccuracy.com/product/borden-timberline-receiver-right-hand-repeater-mag-bolt-face-ultra-mag-well/", "Receivers", "Actions"),
    ("Impact 737R – Right Hand – 308", "Impact", "$1,430",
     "https://gtaccuracy.com/wp-content/uploads/2026/04/737-Right.webp",
     "https://gtaccuracy.com/product/impact-737r-right-hand-308-bolt-face-75-degree-handle/", "Receivers", "Actions"),
    ("Kelbly Prometheus – RH 308", "Kelbly", "$1,400",
     "https://gtaccuracy.com/wp-content/uploads/2025/06/Kelbly-Prometheus-Shots-9.jpg",
     "https://gtaccuracy.com/product/kelbly-prometheus-right-hand-308-bolt-face/", "Receivers", "Actions"),
    ("Borden Bottom Lug", "Borden", "$75",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/IMG_8428.jpeg",
     "https://gtaccuracy.com/product/borden-bottom-lug/", "Receivers", "Accessories"),
    ("Borden Pinned Lug", "Borden", "$75",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden_PinnedLug.webp",
     "https://gtaccuracy.com/product/borden-pinned-lug/", "Receivers", "Accessories"),
    ("Borden BR Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-BR-Rails.webp",
     "https://gtaccuracy.com/product/borden-br-rail-20-moa/", "Receivers", "Rails"),
    ("Borden BRL Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-BR-Rails.webp",
     "https://gtaccuracy.com/product/borden-brl-rail-20-moa/", "Receivers", "Rails"),
    ("Borden BRLXD Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-BR-Rails.webp",
     "https://gtaccuracy.com/product/borden-brlxd-rail-20-moa/", "Receivers", "Rails"),
    ("Borden BRM Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-BR-Rails.webp",
     "https://gtaccuracy.com/product/borden-brm-rail-20-moa/", "Receivers", "Rails"),
    ("Borden BRMXD Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-BR-Rails.webp",
     "https://gtaccuracy.com/product/borden-brmxd-rail-20-moa/", "Receivers", "Rails"),
    ("Borden LA Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-Rem700_Rail.webp",
     "https://gtaccuracy.com/product/borden-la-rail-20-moa/", "Receivers", "Rails"),
    ("Borden Ridge Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-Rem700_Rail.webp",
     "https://gtaccuracy.com/product/borden-ridge-rail-20-moa/", "Receivers", "Rails"),
    ("Borden SA Rail – 20 MOA", "Borden", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2024/05/Borden-Rem700_Rail.webp",
     "https://gtaccuracy.com/product/borden-sa-rail-20-moa/", "Receivers", "Rails"),
    ("BAT 2-Screw Kit", "BAT", "$14.50",
     "https://gtaccuracy.com/wp-content/uploads/2024/12/BAT-Screws-L_S.jpg",
     "https://gtaccuracy.com/product/bat-2-screw-kit/", "Receivers", "Accessories"),
    ("BAT 2-Screw Kit – Radial", "BAT", "$18", None,
     "https://gtaccuracy.com/product/bat-2-screw-kit-radial/", "Receivers", "Accessories"),
    ("3D Inletting – BAT B", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-bat-b/", "Receivers", "3D Inletting"),
    ("3D Inletting – BAT M 1.400 Multi-Flat", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-bat-m/", "Receivers", "3D Inletting"),
    ("3D Inletting – BAT M 1.550", "GT Accuracy", "$25", None,
     "https://gtaccuracy.com/product/3d-inletting-models-bat-m-1550/", "Receivers", "3D Inletting"),
    ("3D Inletting – Borden BR", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-borden-br/", "Receivers", "3D Inletting"),
    ("3D Inletting – Borden BRL", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-borden-brl/", "Receivers", "3D Inletting"),
    ("3D Inletting – Borden BRLXD", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-borden-brlxd/", "Receivers", "3D Inletting"),
    ("3D Inletting – Borden BRM", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-borden-brm/", "Receivers", "3D Inletting"),
    ("3D Inletting – Borden BRMXD", "GT Accuracy", "$20",
     "https://gtaccuracy.com/wp-content/uploads/2025/11/BordenBRMXD-2.jpg",
     "https://gtaccuracy.com/product/3d-inletting-models-borden-brmxd/", "Receivers", "3D Inletting"),
    ("3D Inletting – Kelbly Panda", "GT Accuracy", "$20", None,
     "https://gtaccuracy.com/product/3d-inletting-models-kelbly-panda/", "Receivers", "3D Inletting"),

    # ── STOCKS ────────────────────────────────────────────────
    ("GTA Stockworks Lowrider XL Stock", "GTA Stockworks", "$1,099",
     "https://gtaccuracy.com/wp-content/uploads/2024/03/GTA-LR-BlueWave.jpg",
     "https://gtaccuracy.com/product/gta-stockworks-lowrider-xl-stock/", "Stocks", "Stocks"),
    ("GTA ADL Trigger Guard", "GT Accuracy", "$45",
     "https://gtaccuracy.com/wp-content/uploads/2024/12/GTA_Triger_Guard-1Hole.webp",
     "https://gtaccuracy.com/product/gta-adl-trigger-guard/", "Stocks", "Hardware"),

    # ── TRIGGERS ──────────────────────────────────────────────
    ("Bix'n Andy Dakota – Rem 700", "Bix'n Andy", "$199",
     "https://gtaccuracy.com/wp-content/uploads/2024/11/TRBX0103.jpg",
     "https://gtaccuracy.com/product/bixn-andy-dakota-trigger-remington-700-top-right-safety/", "Triggers", "Triggers"),
    ("Bix'n Andy Rem 700 Competition – No Safety", "Bix'n Andy", "$540",
     "https://gtaccuracy.com/wp-content/uploads/2024/11/TRBX0001.jpg",
     "https://gtaccuracy.com/product/bixn-andy-remington-700-competition-trigger-no-safety/", "Triggers", "Triggers"),
    ("Bix'n Andy Rem 700 TacSport PRO X", "Bix'n Andy", "$375",
     "https://gtaccuracy.com/wp-content/uploads/2024/11/TRBX0112.jpg",
     "https://gtaccuracy.com/product/bixn-andy-remington-700-tacsport-pro-x-single-stage-top-right-safety-w-gator-shoe/", "Triggers", "Triggers"),
    ("TriggerTech Rem 700 Diamond – Flat Shoe", "TriggerTech", "$316.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/R70-SRB-02-TNF_1.webp",
     "https://gtaccuracy.com/product/remington-700-diamond-trigger-right-hand-black-pvd-flat-shoe/", "Triggers", "Triggers"),
    ("TriggerTech Rem 700 Diamond – Pro Curved", "TriggerTech", "$316.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/R70-SRB-02-TNP_1.webp",
     "https://gtaccuracy.com/product/remington-700-diamond-trigger-right-hand-black-pvd-pro-curved-shoe/", "Triggers", "Triggers"),

    # ── SILENCERS ─────────────────────────────────────────────
    ("Diligent Defense Enticer L – Mill Finish", "Diligent Defense", "$600",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Enticer-L-MF.webp",
     "https://gtaccuracy.com/product/diligent-defense-enticer-l-mf/", "Silencers", "Suppressors"),
    ("Diligent Defense Enticer L-Ti – Mill Finish", "Diligent Defense", "$850",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Enticer-LTI-Mill-Finish.webp",
     "https://gtaccuracy.com/product/diligent-defense-enticer-l-ti-mill-finish/", "Silencers", "Suppressors"),
    ("Diligent Defense Enticer S-Ti – Black Cerakote", "Diligent Defense", "$765",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Enticer_S-Blk.webp",
     "https://gtaccuracy.com/product/diligent-defense-enticer-s-ti-black-cerakote/", "Silencers", "Suppressors"),
    ("Diligent Defense Wolf Hunter", "Diligent Defense", "$800",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Wolf-Hunter-w_DTA_2.webp",
     "https://gtaccuracy.com/product/diligent-defense-wolf-hunter/", "Silencers", "Suppressors"),
    ("Huxwrx Flow – 6K", "Huxwrx", "$1,259",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Huxwrx-Flow-6K.webp",
     "https://gtaccuracy.com/product/huxwrx-flow-6k/", "Silencers", "Suppressors"),
    ("PTR Vent 1 Suppressor", "PTR Industries", "$1,499.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/03/VENT1-3.webp",
     "https://gtaccuracy.com/product/ptr-vent-1-suppressor/", "Silencers", "Suppressors"),

    # ── RELOADING ─────────────────────────────────────────────
    ("Alliant Reloader 15.5 – 8 LB", "Alliant", "$479.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/08/Reloader15_5.jpg",
     "https://gtaccuracy.com/product/alliant-reloader-15-5-8-lb/", "Reloading", "Powder"),
    ("Alliant Reloader 16 – 8 LB", "Alliant", "$650",
     "https://gtaccuracy.com/wp-content/uploads/2025/08/Reloader-16.avif",
     "https://gtaccuracy.com/product/alliant-reloader-16-8-lb/", "Reloading", "Powder"),
    ("Alpha 22 GT Brass", "Alpha", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Alpha-22-GT-SRP.jpeg",
     "https://gtaccuracy.com/product/alpha-22-gt/", "Reloading", "Brass"),
    ("Alpha 6mm Creedmoor – LRP", "Alpha", "$130",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Alpha-6-Creedmoor-LRP.jpg",
     "https://gtaccuracy.com/product/alpha-6mm-creedmoor-large-rifle-primer/", "Reloading", "Brass"),
    ("Alpha 6mm Creedmoor – SRP", "Alpha", "$130",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Alpha-6-Creedmoor-SRP.jpg",
     "https://gtaccuracy.com/product/alpha-6mm-creedmoor-small-rifle-primer/", "Reloading", "Brass"),
    ("Alpha 6mm Dasher Brass", "Alpha", "$125",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Alpha-6mm-Dasher.jpeg",
     "https://gtaccuracy.com/product/alpha-6mm-dasher-brass/", "Reloading", "Brass"),
    ("Alpha 6mm PPC Brass", "Alpha", "$160",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Alpha-6ppc.jpg",
     "https://gtaccuracy.com/product/alpha-6mm-ppc-brass/", "Reloading", "Brass"),
    ("Berger 30 cal 200.20x Hybrid Target – 500 ct", "Berger", "$363.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/30_Caliber_200.20x_Hybrid_Target.jpg",
     "https://gtaccuracy.com/product/berger-30-cal-200-20x-hybrid-target-500-pk/", "Reloading", "Bullets"),
    ("Berger 6.5mm 140gr Hybrid Target – 500 ct", "Berger", "$270",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/6.5_mm_140_Grain_Hybrid_Target.jpg",
     "https://gtaccuracy.com/product/berger-6-5mm-140-gr-hybrid-target-500-pk/", "Reloading", "Bullets"),
    ("Berger 6mm 105gr Hybrid Target", "Berger", "$57.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/6_mm_105_Grain_Hybrid_Target.jpg",
     "https://gtaccuracy.com/product/berger-6mm-105-gr-hybrid-target/", "Reloading", "Bullets"),
    ("Berger 6mm 105gr Hybrid Target – 500 ct", "Berger", "$274.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/6_mm_105_Grain_Hybrid_Target.jpg",
     "https://gtaccuracy.com/product/berger-6mm-105-gr-hybrid-target-500-pk/", "Reloading", "Bullets"),
    ("6.5 Creedmoor – Large Rifle Primer", "GT Accuracy", "$125.84", None,
     "https://gtaccuracy.com/product/6-5-creedmoor-large-rifle-primer/", "Reloading", "Primers"),

    # ── PREDATOR & THERMAL ────────────────────────────────────
    ("Fatboy Elevate 2 Section Tripod", "Fatboy", "$675",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/Elevate_2_Section.webp",
     "https://gtaccuracy.com/product/fatboy-elevate-2-section-tripod/", "Predator", "Tripods"),
    ("Fatboy Elevate 3 Section Tripod", "Fatboy", "$675",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/Elevate_3_Section.webp",
     "https://gtaccuracy.com/product/fatboy-elevate-3-section-tripod/", "Predator", "Tripods"),
    ("Fatboy Invert 50 Ball Head", "Fatboy", "$335",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/50_BallHead.png",
     "https://gtaccuracy.com/product/fatboy-invert-50-ball/", "Predator", "Tripod Heads"),
    ("Fatboy Invert 60 Ball Head", "Fatboy", "$375",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/60_Close.png",
     "https://gtaccuracy.com/product/fatboy-invert-60-ball-head/", "Predator", "Tripod Heads"),
    ("Fatboy Levitate Level Head", "Fatboy", "$335",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/Levitate.webp",
     "https://gtaccuracy.com/product/fatboy-levitate-level-head/", "Predator", "Tripod Heads"),
    ("Fatboy Traverse 2 Section Tripod", "Fatboy", "$595",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/Traverse_2_Section.webp",
     "https://gtaccuracy.com/product/fatboy-traverse-2-section-tripod/", "Predator", "Tripods"),
    ("Fatboy Traverse 3 Section Tripod", "Fatboy", "$595",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/Traverse_3_Section.webp",
     "https://gtaccuracy.com/product/fatboy-traverse-3-section-tripod/", "Predator", "Tripods"),
    ("FoxPro Hellcat", "FoxPro", "$269.95",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/Hellcat-2.jpeg",
     "https://gtaccuracy.com/product/foxpro-hellcat/", "Predator", "Calls"),
    ("FoxPro Hellcat Pro", "FoxPro", "$399.95",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/HellcatPro.jpeg",
     "https://gtaccuracy.com/product/foxpro-hellcat-pro/", "Predator", "Calls"),
    ("FoxPro Shockwave", "FoxPro", "$549.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/ShockwaveOpen.jpeg",
     "https://gtaccuracy.com/product/foxpro-shockwave/", "Predator", "Calls"),
    ("FoxPro X24", "FoxPro", "$549.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/X24_2.jpg",
     "https://gtaccuracy.com/product/foxpro-x24/", "Predator", "Calls"),
    ("FoxPro X360", "FoxPro", "$1,499.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/01/x360.jpeg",
     "https://gtaccuracy.com/product/foxpro-x360/", "Predator", "Calls"),
    ("FoxPro X48", "FoxPro", "$899.95", None,
     "https://gtaccuracy.com/product/foxpro-x48/", "Predator", "Calls"),
    ("iRay Rico RH50R MK2 LRF", "iRay", "$5,499",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/RH50R_Left.jpg",
     "https://gtaccuracy.com/product/iray-rico-rh50r-mk2-lrf/", "Predator", "Thermal"),
    ("NocPix Ace H50R Thermal Scope", "NocPix", "$5,499",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/ACE_H50R.jpg",
     "https://gtaccuracy.com/product/nocpix-ace-h50r-thermal-weapon-scope/", "Predator", "Thermal"),
    ("NocPix Ace S60R Thermal Scope", "NocPix", "$5,499.99",
     "https://gtaccuracy.com/wp-content/uploads/2025/02/ACE-S60R_CapClosed.jpg",
     "https://gtaccuracy.com/product/nocpix-ace-s60r-thermal-weapon-scope/", "Predator", "Thermal"),
    ("NocPix Lumi H35 Monocular", "NocPix", "$2,199",
     "https://gtaccuracy.com/wp-content/uploads/2025/11/LUMI_H35_2k_A1_CapOpen__15476.1731622249.1280.1280__64999.jpg",
     "https://gtaccuracy.com/product/nocpix-lumi-h35-monocular/", "Predator", "Thermal"),
    ("NocPix Rico 2 – S75R", "NocPix", "$7,999",
     "https://gtaccuracy.com/wp-content/uploads/2025/11/Nocpix_RICO2_S75R_2k_A1_CapOpen__70486.jpg",
     "https://gtaccuracy.com/product/nocpix-rico-2-s75r/", "Predator", "Thermal"),
    ("NocPix Vista H35R Monocular", "NocPix", "$2,699",
     "https://gtaccuracy.com/wp-content/uploads/2025/11/VISTA-H35R_2k_A1-OpenCap__56717.1738175534.1280.1280__69699.jpg",
     "https://gtaccuracy.com/product/nocpix-vista-h35r-thermal-monocular/", "Predator", "Thermal"),
    ("NocPix Vista H50R Monocular", "NocPix", "$2,399",
     "https://gtaccuracy.com/wp-content/uploads/2025/11/VISTA_H50R_2k_A1_CapOpen__78189.1731623705.1280.1280__90788.jpg",
     "https://gtaccuracy.com/product/nocpix-vista-h50r-thermal-monocular-copy/", "Predator", "Thermal"),
]


def img_local_name(url):
    """Local filename for a given URL."""
    if url is None:
        return None
    return os.path.basename(urllib.parse.urlparse(url).path)


def download_one(url):
    name = img_local_name(url)
    if name is None:
        return None, None
    path = os.path.join(SHOP_DIR, name)
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return url, name  # already have it
    # try full-res first, then -300x300 thumbnail
    for try_url in [url, url.replace(".jpg", "-300x300.jpg").replace(".jpeg", "-300x300.jpeg").replace(".webp", "-300x300.webp").replace(".png", "-300x300.png").replace(".avif", "-300x300.avif")]:
        try:
            req = urllib.request.Request(try_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
            if len(data) > 2000:
                with open(path, "wb") as f:
                    f.write(data)
                return url, name
        except Exception:
            continue
    return url, None  # failed


# Collect unique URLs and download
unique_urls = sorted({p[3] for p in PRODUCTS if p[3]})
print(f"Downloading {len(unique_urls)} unique images...")
results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for url, fname in ex.map(download_one, unique_urls):
        results[url] = fname

failed = [u for u, f in results.items() if f is None]
print(f"OK: {len(unique_urls) - len(failed)}    FAILED: {len(failed)}")
for u in failed[:10]:
    print("  -", u)


# Build HTML for each category
CATEGORIES = [
    ("Rifles", "01", "Custom & Production Rifles", "GTA hand-builds and select factory rifles"),
    ("Barrels", "02", "Barrels", "Cut-rifled blanks and prefit chambers"),
    ("Receivers", "03", "Receivers & Hardware", "Borden, BAT, Impact, Kelbly — actions, rails, lugs, and 3D inletting models"),
    ("Stocks", "04", "Stocks", "GTA Stockworks + hardware"),
    ("Triggers", "05", "Triggers", "Bix'n Andy and TriggerTech"),
    ("Silencers", "06", "Silencers", "Diligent Defense, Huxwrx, PTR"),
    ("Reloading", "07", "Reloading", "Brass, bullets, powder, primers"),
    ("Predator", "08", "Predator & Thermal", "Calls, tripods, and thermal optics"),
]


def render_card(p):
    name, brand, price, img_url, prod_url, cat, sub = p
    local = results.get(img_url) if img_url else None
    if local:
        img_html = f'<div class="product-img"><img src="assets/images/shop/{local}" alt="{name}" loading="lazy" /></div>'
    else:
        img_html = '<div class="product-img product-img--logo"><img src="assets/images/logo.png" alt="GT Accuracy" loading="lazy" /></div>'
    # escape & in names for HTML
    safe_name = name.replace("&", "&amp;")
    return f'''<article class="product">
  {img_html}
  <div class="product-meta">
    <span class="m">{brand.upper()}</span>
    <h3>{safe_name}</h3>
    <span class="sub">{sub}</span>
    <span class="price">{price}</span>
  </div>
</article>'''


sections = []
for cat_key, num, title, desc in CATEGORIES:
    items = [p for p in PRODUCTS if p[5] == cat_key]
    if not items:
        continue
    cards = "\n      ".join(render_card(p) for p in items)
    sections.append(f'''    <div class="catalog-group" id="cat-{cat_key.lower()}">
      <div class="group-head">
        <span class="group-num">{num}</span>
        <h3 class="group-title">{title}</h3>
        <span class="group-meta">{len(items)} items &middot; {desc}</span>
      </div>
      <div class="featured-grid">
      {cards}
      </div>
    </div>''')

catalog_inner = "\n".join(sections)
total = len(PRODUCTS)

# Write a small fragment we can splice into catalog.html
with open("catalog_fragment.html", "w") as f:
    f.write(catalog_inner)

print(f"\nGenerated catalog HTML with {total} products in {len(sections)} sections")
print("Fragment written to catalog_fragment.html")
