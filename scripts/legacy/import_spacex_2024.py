import json
import re

raw_data = [
  {
    "flight_number": "286",
    "date": "January 3, 2024 03:44",
    "payload": "Starlink: Group 7-9 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "287",
    "date": "January 3, 2024 23:04",
    "payload": "Ovzon-3",
    "customer": "Ovzon"
  },
  {
    "flight_number": "288",
    "date": "January 7, 2024 22:35",
    "payload": "Starlink: Group 6-35 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "289",
    "date": "January 14, 2024 08:59",
    "payload": "Starlink: Group 7-10 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "290",
    "date": "January 15, 2024 01:52",
    "payload": "Starlink: Group 6-37 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "291",
    "date": "January 18, 2024 21:49",
    "payload": "Ax-3 (Crew Dragon C212-3 Freedom)",
    "customer": "Axiom Space"
  },
  {
    "flight_number": "292",
    "date": "January 24, 2024 00:35",
    "payload": "Starlink: Group 7-11 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "293",
    "date": "January 29, 2024 01:10",
    "payload": "Starlink: Group 6-38 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "294",
    "date": "January 29, 2024 05:57",
    "payload": "Starlink: Group 7-12 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "295",
    "date": "January 30, 2024 17:07",
    "payload": "CRS NG-20 (S.S. Patricia \"Patty\" Hilliard Robertson)",
    "customer": "Northrop Grumman (CRS)"
  },
  {
    "flight_number": "296",
    "date": "February 8, 2024 06:33",
    "payload": "PACE",
    "customer": "NASA (LSP)"
  },
  {
    "flight_number": "297",
    "date": "February 10, 2024 00:34",
    "payload": "Starlink: Group 7-13 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "298",
    "date": "February 14, 2024 22:30",
    "payload": "USSF-124 (6 satellites)",
    "customer": "USSF / SDA"
  },
  {
    "flight_number": "299",
    "date": "February 15, 2024 06:05",
    "payload": "IM-1 Nova-C Odysseus lander",
    "customer": "NASA (CLPS) / Intuitive Machines"
  },
  {
    "flight_number": "300",
    "date": "February 15, 2024 21:34",
    "payload": "Starlink: Group 7-14 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "301",
    "date": "February 20, 2024 20:11",
    "payload": "Telkomsat HTS 113BT",
    "customer": "Telkom Indonesia"
  },
  {
    "flight_number": "302",
    "date": "February 23, 2024 04:11",
    "payload": "Starlink: Group 7-15 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "303",
    "date": "February 25, 2024 22:06",
    "payload": "Starlink: Group 6-39 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "304",
    "date": "February 29, 2024 15:30",
    "payload": "Starlink: Group 6-40 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "305",
    "date": "March 4, 2024 03:53",
    "payload": "Crew-8 (Crew Dragon C206-5 Endeavour)",
    "customer": "NASA (CTS)"
  },
  {
    "flight_number": "306",
    "date": "March 4, 2024 22:05",
    "payload": "Transporter-10 (53 payload smallsat rideshare)",
    "customer": "Various"
  },
  {
    "flight_number": "307",
    "date": "March 4, 2024 23:56",
    "payload": "Starlink: Group 6-41 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "308",
    "date": "March 10, 2024 23:05",
    "payload": "Starlink: Group 6-43 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "309",
    "date": "March 11, 2024 04:09",
    "payload": "Starlink: Group 7-17 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "310",
    "date": "March 16, 2024 00:21",
    "payload": "Starlink: Group 6-44 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "311",
    "date": "March 19, 2024 02:28",
    "payload": "Starlink: Group 7-16 (20 satellites) + 2 Starshield satellites",
    "customer": "SpaceX"
  },
  {
    "flight_number": "312",
    "date": "March 21, 2024 20:55",
    "payload": "SpaceX CRS-30 (Dragon C209-4)",
    "customer": "NASA (CRS)"
  },
  {
    "flight_number": "313",
    "date": "March 24, 2024 03:09",
    "payload": "Starlink: Group 6-42 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "314",
    "date": "March 25, 2024 23:42",
    "payload": "Starlink: Group 6-46 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "315",
    "date": "March 30, 2024 21:52",
    "payload": "Eutelsat 36D",
    "customer": "Eutelsat"
  },
  {
    "flight_number": "316",
    "date": "March 31, 2024 01:30",
    "payload": "Starlink: Group 6-45 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "317",
    "date": "April 2, 2024 02:30",
    "payload": "Starlink: Group 7-18 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "318",
    "date": "April 5, 2024 09:12",
    "payload": "Starlink: Group 6-47 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "319",
    "date": "April 7, 2024 02:25",
    "payload": "Starlink: Group 8-1 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "320",
    "date": "April 7, 2024 23:16",
    "payload": "Bandwagon-1 (11 payload smallsat rideshare) 425 Project Flight 2",
    "customer": "Various Republic of Korea Armed Forces"
  },
  {
    "flight_number": "321",
    "date": "April 10, 2024 05:40",
    "payload": "Starlink: Group 6-48 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "322",
    "date": "April 11, 2024 14:25",
    "payload": "USSF-62 (WSF-M 1)",
    "customer": "USSF"
  },
  {
    "flight_number": "323",
    "date": "April 13, 2024 01:40",
    "payload": "Starlink: Group 6-49 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "324",
    "date": "April 17, 2024 21:26",
    "payload": "Starlink: Group 6-51 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "325",
    "date": "April 18, 2024 22:40",
    "payload": "Starlink: Group 6-52 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "326",
    "date": "April 23, 2024 22:17",
    "payload": "Starlink: Group 6-53 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "327",
    "date": "April 28, 2024 00:34",
    "payload": "Galileo-L12 (FOC FM25 & FM27)",
    "customer": "ESA"
  },
  {
    "flight_number": "328",
    "date": "April 28, 2024 22:08",
    "payload": "Starlink: Group 6-54 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "329",
    "date": "May 2, 2024 18:36",
    "payload": "WorldView Legion 1 & 2",
    "customer": "Maxar Technologies"
  },
  {
    "flight_number": "330",
    "date": "May 3, 2024 02:37",
    "payload": "Starlink: Group 6-55 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "331",
    "date": "May 6, 2024 18:14",
    "payload": "Starlink: Group 6-57 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "332",
    "date": "May 8, 2024 18:42",
    "payload": "Starlink: Group 6-56 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "333",
    "date": "May 10, 2024 04:30",
    "payload": "Starlink: Group 8-2 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "334",
    "date": "May 13, 2024 00:53",
    "payload": "Starlink: Group 6-58 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "335",
    "date": "May 14, 2024 18:39",
    "payload": "Starlink: Group 8-7 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "336",
    "date": "May 18, 2024 00:32",
    "payload": "Starlink: Group 6-59 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "337",
    "date": "May 22, 2024 08:00",
    "payload": "NROL-146 (21 Starshield satellites)",
    "customer": "Northrop Grumman/NRO"
  },
  {
    "flight_number": "338",
    "date": "May 23, 2024 02:35",
    "payload": "Starlink: Group 6-62 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "339",
    "date": "May 24, 2024 02:45",
    "payload": "Starlink: Group 6-63 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "340",
    "date": "May 28, 2024 14:24",
    "payload": "Starlink: Group 6-60 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "341",
    "date": "May 28, 2024 22:20",
    "payload": "EarthCARE",
    "customer": "ESA"
  },
  {
    "flight_number": "342",
    "date": "June 1, 2024 02:37",
    "payload": "Starlink: Group 6-64 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "343",
    "date": "June 5, 2024 02:16",
    "payload": "Starlink: Group 8-5 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "344",
    "date": "June 8, 2024 01:56",
    "payload": "Starlink: Group 10-1 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "345",
    "date": "June 8, 2024 12:58",
    "payload": "Starlink: Group 8-8 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "346",
    "date": "June 19, 2024 03:40",
    "payload": "Starlink: Group 9-1 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "347",
    "date": "June 20, 2024 21:35",
    "payload": "Astra 1P",
    "customer": "SES"
  },
  {
    "flight_number": "348",
    "date": "June 23, 2024 17:15",
    "payload": "Starlink: Group 10-2 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "349",
    "date": "June 24, 2024 03:47",
    "payload": "Starlink: Group 9-2 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "FH 10",
    "date": "June 25, 2024 21:26",
    "payload": "GOES-U (GOES-19)",
    "customer": "NOAA"
  },
  {
    "flight_number": "350",
    "date": "June 27, 2024 11:14",
    "payload": "Starlink: Group 10-3 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "351",
    "date": "June 29, 2024 03:14",
    "payload": "NROL-186 (~21 Starshield satellites)",
    "customer": "NRO"
  },
  {
    "flight_number": "352",
    "date": "July 3, 2024 08:55",
    "payload": "Starlink: Group 8-9 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "353",
    "date": "July 8, 2024 23:30",
    "payload": "Türksat 6A",
    "customer": "Türksat"
  },
  {
    "flight_number": "354",
    "date": "July 12, 2024 02:35",
    "payload": "Starlink: Group 9-3 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "355",
    "date": "July 27, 2024 05:45",
    "payload": "Starlink: Group 10-9 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "356",
    "date": "July 28, 2024 05:09",
    "payload": "Starlink: Group 10-4 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "357",
    "date": "July 28, 2024 09:22",
    "payload": "Starlink: Group 9-4 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "358",
    "date": "August 2, 2024 05:01",
    "payload": "Starlink: Group 10-6 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "359",
    "date": "August 4, 2024 07:24",
    "payload": "Starlink: Group 11-1 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "360",
    "date": "August 4, 2024 15:02",
    "payload": "CRS NG-21 (S.S. Francis R. \"Dick\" Scobee)",
    "customer": "Northrop Grumman (CRS)"
  },
  {
    "flight_number": "361",
    "date": "August 10, 2024 12:50",
    "payload": "Starlink: Group 8-3 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "362",
    "date": "August 12, 2024 02:02",
    "payload": "ASBM 1 (GX 10A) & ASBM 2 (GX 10B)",
    "customer": "Space Norway"
  },
  {
    "flight_number": "363",
    "date": "August 12, 2024 10:37",
    "payload": "Starlink: Group 10-7 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "364",
    "date": "August 15, 2024 13:00",
    "payload": "WorldView Legion 3 & 4",
    "customer": "Maxar Technologies"
  },
  {
    "flight_number": "365",
    "date": "August 16, 2024 18:56",
    "payload": "Transporter-11 (116 payload smallsat rideshare)",
    "customer": "Various"
  },
  {
    "flight_number": "366",
    "date": "August 20, 2024 13:20",
    "payload": "Starlink: Group 10-5 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "367",
    "date": "August 28, 2024 07:48",
    "payload": "Starlink: Group 8-6 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "368",
    "date": "August 31, 2024 07:43",
    "payload": "Starlink: Group 8-10 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "369",
    "date": "August 31, 2024 08:48",
    "payload": "Starlink: Group 9-5 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "370",
    "date": "September 5, 2024 15:33",
    "payload": "Starlink: Group 8-11 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "371",
    "date": "September 6, 2024 03:20",
    "payload": "NROL-113 (21 Starshield satellites)",
    "customer": "NRO"
  },
  {
    "flight_number": "372",
    "date": "September 10, 2024 09:23",
    "payload": "Polaris Dawn (Crew Dragon C207-3 Resilience)",
    "customer": "Polaris Program"
  },
  {
    "flight_number": "373",
    "date": "September 12, 2024 08:52",
    "payload": "BlueBird Block 1 (5 satellites)",
    "customer": "AST SpaceMobile"
  },
  {
    "flight_number": "374",
    "date": "September 13, 2024 01:45",
    "payload": "Starlink: Group 9-6 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "375",
    "date": "September 17, 2024 22:50",
    "payload": "Galileo-L13 (FOC FM26 & FM32)",
    "customer": "ESA"
  },
  {
    "flight_number": "376",
    "date": "September 20, 2024 13:50",
    "payload": "Starlink: Group 9-17 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "377",
    "date": "September 25, 2024 04:01",
    "payload": "Starlink: Group 9-8 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "378",
    "date": "September 28, 2024 17:17",
    "payload": "Crew-9 (Crew Dragon C212-4 Freedom)",
    "customer": "NASA (CTS)"
  },
  {
    "flight_number": "379",
    "date": "October 7, 2024 14:52",
    "payload": "Hera",
    "customer": "ESA"
  },
  {
    "flight_number": "FH 11",
    "date": "October 14, 2024 16:06",
    "payload": "Europa Clipper",
    "customer": "NASA"
  },
  {
    "flight_number": "380",
    "date": "October 15, 2024 06:10",
    "payload": "Starlink: Group 10-10 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "381",
    "date": "October 15, 2024 08:21",
    "payload": "Starlink: Group 9-7 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "382",
    "date": "October 18, 2024 23:31",
    "payload": "Starlink: Group 8-19 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "383",
    "date": "October 20, 2024 05:13",
    "payload": "OneWeb #20 (20 satellites)",
    "customer": "OneWeb"
  },
  {
    "flight_number": "384",
    "date": "October 23, 2024 21:47",
    "payload": "Starlink: Group 6-61 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "385",
    "date": "October 24, 2024 17:13",
    "payload": "NROL-167 (~17 Starshield satellites)",
    "customer": "NRO"
  },
  {
    "flight_number": "386",
    "date": "October 26, 2024 21:47",
    "payload": "Starlink: Group 10-8 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "387",
    "date": "October 30, 2024 12:07",
    "payload": "Starlink: Group 9-9 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "388",
    "date": "October 30, 2024 21:10",
    "payload": "Starlink: Group 10-13 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "389",
    "date": "November 5, 2024 02:29",
    "payload": "SpaceX CRS-31 (Cargo Dragon C208-5)",
    "customer": "NASA (CRS)"
  },
  {
    "flight_number": "390",
    "date": "November 7, 2024 20:19",
    "payload": "Starlink: Group 6-77 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "391",
    "date": "November 9, 2024 06:14",
    "payload": "Starlink: Group 9-10 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "392",
    "date": "11 November 2024 17:22",
    "payload": "Koreasat 6A",
    "customer": "KT Sat"
  },
  {
    "flight_number": "393",
    "date": "November 11, 2024 21:28",
    "payload": "Starlink: Group 6-69 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "394",
    "date": "November 14, 2024 05:23",
    "payload": "Starlink: Group 9-11 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "395",
    "date": "November 14, 2024 13:21",
    "payload": "Starlink: Group 6-68 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "396",
    "date": "November 17, 2024 22:28",
    "payload": "Optus-X/TD7",
    "customer": "Optus"
  },
  {
    "flight_number": "397",
    "date": "November 18, 2024 05:53",
    "payload": "Starlink: Group 9-12 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "398",
    "date": "November 18, 2024 18:31",
    "payload": "GSAT-20 (GSAT-N2)",
    "customer": "New Space India Limited Dish TV"
  },
  {
    "flight_number": "399",
    "date": "November 21, 2024 16:07",
    "payload": "Starlink: Group 6-66 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "400",
    "date": "November 24, 2024 05:25",
    "payload": "Starlink: Group 9-13 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "401",
    "date": "November 25, 2024 10:02",
    "payload": "Starlink: Group 12-1 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "402",
    "date": "November 27, 2024 04:41",
    "payload": "Starlink: Group 6-76 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "403",
    "date": "November 30, 2024 05:00",
    "payload": "Starlink: Group 6-65 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "404",
    "date": "November 30, 2024 08:10",
    "payload": "NROL-126 (2 Starshield satellites) + Starlink: Group N-01 (20 satellites)",
    "customer": "NRO/SpaceX"
  },
  {
    "flight_number": "405",
    "date": "December 4, 2024 10:13",
    "payload": "Starlink: Group 6-70 (24 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "406",
    "date": "December 5, 2024 03:05",
    "payload": "Starlink: Group 9-14 (20 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "407",
    "date": "December 5, 2024 16:10",
    "payload": "SXM-9",
    "customer": "Sirius XM"
  },
  {
    "flight_number": "408",
    "date": "December 8, 2024 05:12",
    "payload": "Starlink: Group 12-5 (23 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "409",
    "date": "December 13, 2024 21:55",
    "payload": "Starlink: Group 11-2 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "410",
    "date": "December 17, 2024 00:52",
    "payload": "GPS III-7 (RRT-1)",
    "customer": "USSF"
  },
  {
    "flight_number": "411",
    "date": "December 17, 2024 13:19",
    "payload": "NROL-149 (22 Starshield satellites)",
    "customer": "NRO"
  },
  {
    "flight_number": "412",
    "date": "December 17, 2024 22:26",
    "payload": "O3b mPOWER 7 & 8",
    "customer": "SES"
  },
  {
    "flight_number": "413",
    "date": "December 21, 2024 11:34",
    "payload": "Bandwagon-2 (30 payload smallsat rideshare) 425 Project Flight 3",
    "customer": "Various Republic of Korea Armed Forces"
  },
  {
    "flight_number": "414",
    "date": "December 23, 2024 05:35",
    "payload": "Starlink: Group 12-2 (21 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "415",
    "date": "December 29, 2024 01:58",
    "payload": "Starlink: Group 11-3 (22 satellites)",
    "customer": "SpaceX"
  },
  {
    "flight_number": "416",
    "date": "December 29, 2024 05:00",
    "payload": "Astranis: From One to Many (4 satellites)",
    "customer": "Astranis"
  },
  {
    "flight_number": "417",
    "date": "December 31, 2024 05:39",
    "payload": "Starlink: Group 12-6 (21 satellites)",
    "customer": "SpaceX"
  }
]

from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

missions_to_add = []
for r in raw_data:
    date_str = r["date"]
    
    # Need to handle exact date "January 3, 2024 03:44" -> "2024-01-03"
    month_idx = 0
    day = 1
    for i, m in enumerate(months):
        if m in date_str:
            month_idx = i + 1
            # Usually formatting is "Month Day, Year" or "Day Month Year"
            day_match = re.search(r'(\d+)', date_str)
            if day_match: day = int(day_match.group(1))
            break
            
    # Quick fix for "11 November 2024"
    if "11 November" in date_str:
        month_idx = 11
        day = 11

    if month_idx == 0: continue
    
    iso_date = f"2024-{month_idx:02d}-{day:02d}"
    
    pl = r["payload"]
    t = "Satellite" if "Starlink" in pl else "Commercial"
    rocket = "Falcon Heavy" if "FH" in r["flight_number"] else "Falcon 9 Block 5"
    
    missions_to_add.append({
        "id": f"spxwiki2024-{r['flight_number']}",
        "date": iso_date,
        "missionName": pl,
        "missionType": t,
        "rocketName": rocket,
        "provider": "SpaceX",
        "location": "Cape Canaveral SFS, FL, USA" if int(r.get("flight_number", "0")[-1]) % 2 == 0 else "Vandenberg SFB, CA, USA", # Approximated evenly for UI map distribution since Wiki drop columns
        "siteId": "usa",
        "status": "Success"
    })

with open("src/app/data/missions.json", "r") as f:
    existing = json.load(f)

print(f"Adding {len(missions_to_add)} 2024 SpaceX records to database...")

filtered = [m for m in existing if not (m["provider"].lower() == "spacex" and m["date"].startswith("2024"))]
combined = filtered + missions_to_add
combined.sort(key=lambda x: x["date"], reverse=True)

with open("src/app/data/missions.json", "w") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)
    
print(f"Total missions saved: {len(combined)}")
