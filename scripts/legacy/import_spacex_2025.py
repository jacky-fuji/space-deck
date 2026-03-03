import json
import re

raw_table = """
| Flight No. | Date (UTC) | Launch Site | Payload | Customer |
| :--- | :--- | :--- | :--- | :--- |
| 418 | January 4, 2025 | Cape Canaveral, SLC‑40 | Thuraya 4-NGS | Thuraya |
| 419 | January 6, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6‑71 | SpaceX |
| 420 | January 8, 2025 | Kennedy, LC‑39A | Starlink: Group 12-11 | SpaceX |
| 421 | January 10, 2025 | Vandenberg, SLC‑4E | NROL-153 (22 Starshield) | NRO |
| 422 | January 10, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-12 | SpaceX |
| 423 | January 13, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-4 | SpaceX |
| 424 | January 14, 2025 | Vandenberg, SLC‑4E | Transporter-12 | Various |
| 425 | January 15, 2025 | Kennedy, LC‑39A | Blue Ghost Mission 1 | Firefly/NASA |
| 426 | January 21, 2025 | Kennedy, LC‑39A | Starlink: Group 13-1 | SpaceX |
| 427 | January 21, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-8 | SpaceX |
| 428 | January 24, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-6 | SpaceX |
| 429 | January 27, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-7 | SpaceX |
| 430 | January 30, 2025 | Kennedy, LC‑39A | Spainsat NG I | Hisdesat |
| 431 | February 1, 2025 | Vandenberg, SLC-4E | Starlink: Group 11-4 | SpaceX |
| 432 | February 4, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-3 | SpaceX |
| 433 | February 4, 2025 | Kennedy, LC‑39A | WorldView Legion 5 & 6 | Maxar |
| 434 | February 8, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-9 | SpaceX |
| 435 | February 11, 2025 | Vandenberg, SLC-4E | Starlink: Group 11-10 | SpaceX |
| 436 | February 11, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-18 | SpaceX |
| 437 | February 15, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-8 | SpaceX |
| 438 | February 18, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-12 | SpaceX |
| 439 | February 21, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-14 | SpaceX |
| 440 | February 23, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-1 | SpaceX |
| 441 | February 27, 2025 | Kennedy, LC‑39A | IM-2 Nova-C "Athena" | NASA/Intuitive |
| 442 | February 27, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-13 | SpaceX |
| 443 | March 3, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-20 | SpaceX |
| 444 | March 12, 2025 | Vandenberg, SLC‑4E | SPHEREx / PUNCH | NASA |
| 445 | March 13, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-21 | SpaceX |
| 446 | March 14, 2025 | Kennedy, LC‑39A | Crew-10 | NASA |
| 447 | March 15, 2025 | Vandenberg, SLC‑4E | Transporter-13 | Various |
| 448 | March 15, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-16 | SpaceX |
| 449 | March 18, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-25 | SpaceX |
| 450 | March 21, 2025 | Vandenberg, SLC‑4E | NROL-57 (~11 Starshield) | NRO |
| 451 | March 24, 2025 | Cape Canaveral, SLC‑40 | NROL-69 | USSF |
| 452 | March 26, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-7 | SpaceX |
| 453 | March 31, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-80 | SpaceX |
| 454 | April 1, 2025 | Kennedy, LC‑39A | Fram2 (Crew Dragon) | Chun Wang |
| 455 | April 4, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-13 | SpaceX |
| 456 | April 6, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-72 | SpaceX |
| 457 | April 7, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-11 | SpaceX |
| 458 | April 12, 2025 | Vandenberg, SLC‑4E | NROL-192 (22 Starshield) | NRO |
| 459 | April 13, 2025 | Kennedy, LC‑39A | Starlink: Group 12-17 | SpaceX |
| 460 | April 14, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-73 | SpaceX |
| 461 | April 20, 2025 | Vandenberg, SLC‑4E | NROL-145 (22 Starshield) | NRO |
| 462 | April 21, 2025 | Kennedy, LC‑39A | SpaceX CRS-32 | NASA |
| 463 | April 22, 2025 | Cape Canaveral, SLC‑40 | Bandwagon-3 | Various |
| 464 | April 25, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-74 | SpaceX |
| 465 | April 28, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-23 | SpaceX |
| 466 | April 28, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-9 | SpaceX |
| 467 | April 29, 2025 | Kennedy, LC‑39A | Starlink: Group 12-10 | SpaceX |
| 468 | May 2, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-75 | SpaceX |
| 469 | May 4, 2025 | Kennedy, LC‑39A | Starlink: Group 6-84 | SpaceX |
| 470 | May 7, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-93 | SpaceX |
| 471 | May 10, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-3 | SpaceX |
| 472 | May 10, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-91 | SpaceX |
| 473 | May 13, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-4 | SpaceX |
| 474 | May 13, 2025 | Kennedy, LC‑39A | Starlink: Group 6-83 | SpaceX |
| 475 | May 14, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-67 | SpaceX |
| 476 | May 16, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-5 | SpaceX |
| 477 | May 21, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-15 | SpaceX |
| 478 | May 23, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-16 | SpaceX |
| 479 | May 24, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-22 | SpaceX |
| 480 | May 27, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-1 | SpaceX |
| 481 | May 28, 2025 | Kennedy, LC‑39A | Starlink: Group 10-32 | SpaceX |
| 482 | May 30, 2025 | Cape Canaveral, SLC‑40 | GPS III-8 | USSF |
| 483 | May 31, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-18 | SpaceX |
| 484 | June 3, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-19 | SpaceX |
| 485 | June 4, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-22 | SpaceX |
| 486 | June 7, 2025 | Cape Canaveral, SLC‑40 | SXM-10 | Sirius XM |
| 487 | June 8, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-8 | SpaceX |
| 488 | June 10, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-24 | SpaceX |
| 489 | June 13, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-6 | SpaceX |
| 490 | June 13, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 12-26 | SpaceX |
| 491 | June 17, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-9 | SpaceX |
| 492 | June 18, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-18 | SpaceX |
| 493 | June 23, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-23 | SpaceX |
| 494 | June 23, 2025 | Vandenberg, SLC‑4E | Transporter-14 | Various |
| 495 | June 25, 2025 | Kennedy, LC‑39A | Axiom Mission 4 | Axiom Space |
| 496 | June 25, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-16 | SpaceX |
| 497 | June 28, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-34 | SpaceX |
| 498 | June 28, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-7 | SpaceX |
| 499 | July 1, 2025 | Kennedy, LC‑39A | MTG-S1 / Sentinel-4A | EUMETSAT |
| 500 | July 2, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-25 | SpaceX |
| 501 | July 8, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-28 | SpaceX |
| 502 | July 13, 2025 | Cape Canaveral, SLC‑40 | Dror-1 | IAI |
| 503 | July 16, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-2 | SpaceX |
| 504 | July 16, 2025 | Cape Canaveral, SLC‑40 | KuiperSat x 24 (KF-01) | Amazon |
| 505 | July 19, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-3 | SpaceX |
| 506 | July 22, 2025 | Cape Canaveral, SLC‑40 | O3b mPOWER 9 & 10 | SES |
| 507 | July 23, 2025 | Vandenberg, SLC‑4E | TRACERS | NASA |
| 508 | July 26, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-26 | SpaceX |
| 509 | July 27, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-2 | SpaceX |
| 510 | July 30, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-29 | SpaceX |
| 511 | July 31, 2025 | Vandenberg, SLC‑4E | Starlink: Group 13-4 | SpaceX |
| 512 | August 1, 2025 | Kennedy, LC‑39A | Crew-11 | NASA |
| 513 | August 4, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-30 | SpaceX |
| 514 | August 11, 2025 | Cape Canaveral, SLC‑40 | KuiperSat x 24 (KF-02) | Amazon |
| 515 | August 14, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-4 | SpaceX |
| 516 | August 14, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-20 | SpaceX |
| 517 | August 18, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-5 | SpaceX |
| 518 | August 22, 2025 | Kennedy, LC‑39A | USSF-36 (X-37B OTV-8) | USSF |
| 519 | August 22, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-6 | SpaceX |
| 520 | August 24, 2025 | Cape Canaveral, SLC‑40 | SpaceX CRS-33 | NASA |
| 521 | August 26, 2025 | Vandenberg, SLC‑4E | NAOS | Luxembourg |
| 522 | August 27, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-56 | SpaceX |
| 523 | August 28, 2025 | Kennedy, LC‑39A | Starlink: Group 10-11 | SpaceX |
| 524 | August 30, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-7 | SpaceX |
| 525 | August 31, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-14 | SpaceX |
| 526 | September 3, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-8 | SpaceX |
| 527 | September 3, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-22 | SpaceX |
| 528 | September 5, 2025 | Kennedy, LC‑39A | Starlink: Group 10-57 | SpaceX |
| 529 | September 6, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-9 | SpaceX |
| 530 | September 10, 2025 | Vandenberg, SLC‑4E | SDA Tranche 1 Transport B | SDA |
| 531 | September 12, 2025 | Cape Canaveral, SLC‑40 | Nusantara Lima | PSN |
| 532 | September 13, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-10 | SpaceX |
| 533 | September 14, 2025 | Cape Canaveral, SLC‑40 | CRS NG-23 | Northrop |
| 534 | September 18, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-61 | SpaceX |
| 535 | September 19, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-12 | SpaceX |
| 536 | September 21, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-27 | SpaceX |
| 537 | September 22, 2025 | Vandenberg, SLC‑4E | NROL-48 (~11 Starshield) | NRO |
| 538 | September 24, 2025 | Kennedy, LC‑39A | IMAP | NASA |
| 539 | September 25, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-15 | SpaceX |
| 540 | September 26, 2025 | Vandenberg, SLC‑4E | Starlink: Group 17-11 | SpaceX |
| 541 | September 29, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-20 | SpaceX |
| 542 | October 3, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-39 | SpaceX |
| 543 | October 7, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-59 | SpaceX |
| 544 | October 8, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-17 | SpaceX |
| 545 | October 14, 2025 | Cape Canaveral, SLC‑40 | KuiperSat x 24 (KF-03) | Amazon |
| 546 | October 15, 2025 | Vandenberg, SLC‑4E | SDA Tranche 1 Transport C | SDA |
| 547 | October 16, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-52 | SpaceX |
| 548 | October 19, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-17 | SpaceX |
| 549 | October 19, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-19 | SpaceX |
| 550 | October 22, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-5 | SpaceX |
| 551 | October 24, 2025 | Cape Canaveral, SLC‑40 | Spainsat NG II | Hisdesat |
| 552 | October 25, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-12 | SpaceX |
| 553 | October 26, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-21 | SpaceX |
| 554 | October 28, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-21 | SpaceX |
| 555 | October 29, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 10-37 | SpaceX |
| 556 | October 31, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-23 | SpaceX |
| 557 | November 2, 2025 | Cape Canaveral, SLC‑40 | Bandwagon-4 | Various |
| 558 | November 6, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-81 | SpaceX |
| 559 | November 6, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-14 | SpaceX |
| 560 | November 9, 2025 | Kennedy, LC‑39A | Starlink: Group 10-51 | SpaceX |
| 561 | November 11, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-87 | SpaceX |
| 562 | November 15, 2025 | Kennedy, LC‑39A | Starlink: Group 6-89 | SpaceX |
| 563 | November 15, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-85 | SpaceX |
| 564 | November 17, 2025 | Vandenberg, SLC‑4E | Sentinel-6B | NASA/NOAA |
| 565 | November 19, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-94 | SpaceX |
| 566 | November 21, 2025 | Kennedy, LC‑39A | Starlink: Group 6-78 | SpaceX |
| 567 | November 22, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-79 | SpaceX |
| 568 | November 23, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-30 | SpaceX |
| 569 | November 28, 2025 | Vandenberg, SLC‑4E | Transporter-15 | Various |
| 570 | December 1, 2025 | Kennedy, LC‑39A | Starlink: Group 6-86 | SpaceX |
| 571 | December 2, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-10 | SpaceX |
| 572 | December 2, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-95 | SpaceX |
| 573 | December 4, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-25 | SpaceX |
| 574 | December 7, 2025 | Vandenberg, SLC‑4E | Starlink: Group 11-15 | SpaceX |
| 575 | December 8, 2025 | Kennedy, LC‑39A | Starlink: Group 6-92 | SpaceX |
| 576 | December 9, 2025 | Cape Canaveral, SLC‑40 | NROL-77 | NRO |
| 577 | December 10, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-11 | SpaceX |
| 578 | December 11, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-90 | SpaceX |
| 579 | December 14, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-12 | SpaceX |
| 580 | December 15, 2025 | Cape Canaveral, SLC‑40 | Starlink: Group 6-82 | SpaceX |
| 581 | December 17, 2025 | Kennedy, LC‑39A | Starlink: Group 6-99 | SpaceX |
| 582 | December 17, 2025 | Vandenberg, SLC‑4E | Starlink: Group 15-13 | SpaceX |
"""

from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

missions_to_add = []
for line in raw_table.strip().split('\n'):
    line = line.strip()
    if not line.startswith('|') or 'Flight No.' in line or ':---' in line:
        continue
    
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 5:
        continue
        
    flight_num = parts[0]
    date_str = parts[1]
    site = parts[2]
    pl = parts[3]
    customer = parts[4]
    
    month_idx = 0
    day = 1
    for i, m in enumerate(months):
        if m in date_str:
            month_idx = i + 1
            day_match = re.search(r'(\d+)', date_str)
            if day_match: day = int(day_match.group(1))
            break

    if month_idx == 0: continue
    
    iso_date = f"2025-{month_idx:02d}-{day:02d}"
    
    t = "Satellite" if "Starlink" in pl else "Commercial"
    rocket = "Falcon Heavy" if "FH" in flight_num else "Falcon 9 Block 5"
    
    loc = "USA"
    if "Cape Canaveral" in site or "Kennedy" in site:
        loc = "Cape Canaveral SFS, FL, USA"
    elif "Vandenberg" in site:
        loc = "Vandenberg SFB, CA, USA"
    
    missions_to_add.append({
        "id": f"spxwiki2025-{flight_num}",
        "date": iso_date,
        "missionName": pl,
        "missionType": t,
        "rocketName": rocket,
        "provider": "SpaceX",
        "location": loc,
        "siteId": "usa",
        "status": "Success"
    })

with open("src/app/data/missions.json", "r") as f:
    existing = json.load(f)

print(f"Parsed {len(missions_to_add)} 2025 SpaceX records to database...")

filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and m["date"].startswith("2025"))]
combined = filtered + missions_to_add
combined.sort(key=lambda x: x["date"], reverse=True)

with open("src/app/data/missions.json", "w") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)
    
print(f"Total missions saved: {len(combined)}")
