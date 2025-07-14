// sketch.js
let milestones = [
  { name: "永豐外幣", date: "2025-05-09", key: false },
  { name: "財力證明", date: "2025-05-22", key: true },
  { name: "簽證送件", date: "2025-05-22", key: true },
  { name: "體健", date: "2025-05-23", key: true },
  { name: "下簽", date: "2025-05-27", key: true },
  { name: "打包清單", date: "2025-06-03", key: false },
  { name: "購買清單", date: "2025-06-04", key: false },
  { name: "新IG帳號", date: "2025-06-05", key: false },
  { name: "訂機票", date: "2025-08-04", key: true },
  { name: "訂住宿", date: "2025-08-08", key: true },
  { name: "購物", date: "2025-08-18", key: false },
  { name: "SIM卡", date: "2025-08-22", key: false },
  { name: "永豐消費", date: "2025-08-30", key: false },
  { name: "履歷", date: "2025-09-04", key: false },
  { name: "找工作", date: "2025-09-07", key: true },
  { name: "換澳幣", date: "2025-09-10", key: true },
  { name: "開戶", date: "2025-09-14", key: true },
  { name: "資料備份", date: "2025-09-15", key: false },
  { name: "行前確認", date: "2025-09-17", key: true },
  { name: "行李打包", date: "2025-09-18", key: true },
  { name: "信用卡繳費方式", date: "2025-09-19", key: false },
  { name: "整理家裡", date: "2025-09-20", key: false },
  { name: "門號處理", date: "2025-09-23", key: false },
  { name: "出發", date: "2025-09-25", key: true },
];

let todayDate = new Date();
let minDate, maxDate;
let colors;
let showTable = false;
let button;
let hoveredMilestone = null;

function setup() {
  const cnv = createCanvas(1200, 300);
  cnv.parent("canvasHolder");
  textFont("Inter, sans-serif");
  textAlign(CENTER, CENTER);
  colors = [
    color("#e63946"), // red
    color("#f8f9fa"), // lighter off-white
    color("#a8dadc"), // pale blue
    color("#457b9d"), // medium blue
    color("#1d3557"), // dark blue
  ];

  milestones.push({
    name: "Today",
    date: todayDate.toISOString().split("T")[0],
    key: true,
  });

  let dates = milestones.map((m) => new Date(m.date));
  minDate = new Date(Math.min(...dates));
  maxDate = new Date(Math.max(...dates));

  button = createButton("Toggle Milestone Table");
  button.parent("canvasHolder");
  button.mousePressed(() => toggleTable());
}

function draw() {
  background(colors[1]);
  let margin = 80;
  let y = height / 2 - 10;

  // Enhanced timeline line with gradient effect
  stroke(colors[3]);
  strokeWeight(8);
  line(margin, y, width - margin, y);

  // Add subtle shadow line
  stroke(colors[2]);
  strokeWeight(4);
  line(margin, y + 2, width - margin, y + 2);

  noStroke();
  hoveredMilestone = null;

  milestones.forEach((m, i) => {
    let dateObj = new Date(m.date);
    let x = map(
      dateObj.getTime(),
      minDate.getTime(),
      maxDate.getTime(),
      margin,
      width - margin
    );
    let d = dist(mouseX, mouseY, x, y);
    let isHovered = d < 15;

    if (isHovered) hoveredMilestone = { ...m, x: x, y: y };

    // Color coding: Today = red, key dates = dark blue, others = medium blue
    if (m.name === "Today") fill(colors[0]); // red
    else if (m.key) fill(colors[4]); // dark blue for key dates
    else fill(colors[3]); // medium blue for non-key dates

    let size =
      m.name === "Today"
        ? 20
        : m.key
        ? 16 // larger size for key dates
        : 10; // smaller size for non-key dates

    // Add white outline for better visibility on important dates
    if (m.name === "Today" || m.key) {
      fill(255);
      ellipse(x, y, size + 4);
      if (m.name === "Today") fill(colors[0]);
      else fill(colors[4]);
    }

    ellipse(x, y, size);

    // Calculate D-date from 出發
    let departureDate = milestones.find((ms) => ms.name === "出發").date;
    let dCountdown = Math.round(
      (new Date(departureDate) - new Date(m.date)) / (1000 * 60 * 60 * 24)
    );

    // Show labels only for key dates and Today
    if (m.name === "Today") {
      fill(colors[0]);
      textSize(15);
      textAlign(CENTER);
      // Add text background for better readability
      fill(255, 255, 255, 200);
      rectMode(CENTER);
      rect(x, y - 40, 80, 35, 8);
      fill(colors[0]);
      text(`Today\nD-${Math.max(dCountdown, 0)}`, x, y - 40);
    }

    // Show labels for key dates (when not hovered)
    if (m.key && m.name !== "Today" && !isHovered) {
      fill(colors[4]);
      textSize(12);
      textAlign(CENTER);
      // Add text background
      fill(255, 255, 255, 200);
      rectMode(CENTER);
      let labelWidth = Math.max(textWidth(m.name) + 20, 80);
      rect(x, y - 30, labelWidth, 20, 6);
      fill(colors[4]);
      text(m.name, x, y - 30);
    }

    // Enhanced hover display for key dates
    if (m.key && m.name !== "Today" && isHovered) {
      fill(colors[4]);
      textSize(12);
      textAlign(CENTER);
      // Enhanced hover background
      fill(255, 255, 255, 230);
      rectMode(CENTER);
      rect(x, y - 40, 160, 35, 8);
      fill(colors[4]);
      text(`${m.name}\n${m.date} (D-${Math.max(dCountdown, 0)})`, x, y - 40);
    }
  });

  // Hover tooltip for non-key milestones
  if (
    hoveredMilestone &&
    hoveredMilestone.name !== "Today" &&
    !hoveredMilestone.key
  ) {
    fill(colors[4]);
    textSize(13);
    rectMode(CENTER);
    let boxW = 220;
    let boxH = 50;

    // Enhanced tooltip with shadow and better styling
    fill(0, 0, 0, 20);
    rect(hoveredMilestone.x + 2, hoveredMilestone.y - 58, boxW, boxH, 10);

    fill(255, 255, 255, 250);
    stroke(colors[3]);
    strokeWeight(2);
    rect(hoveredMilestone.x, hoveredMilestone.y - 60, boxW, boxH, 10);

    noStroke();
    fill(colors[3]);
    textAlign(CENTER);
    let departureDate = milestones.find((ms) => ms.name === "出發").date;
    let dCountdown = Math.round(
      (new Date(departureDate) - new Date(hoveredMilestone.date)) /
        (1000 * 60 * 60 * 24)
    );
    text(
      `${hoveredMilestone.name}\n${hoveredMilestone.date} (D-${Math.max(
        dCountdown,
        0
      )})`,
      hoveredMilestone.x,
      hoveredMilestone.y - 60
    );
  }

  // Simple hover tooltip for key milestones (just showing date)
  if (
    hoveredMilestone &&
    hoveredMilestone.key &&
    hoveredMilestone.name !== "Today"
  ) {
    // This is handled in the main loop above with enhanced display
  }
}

function toggleTable() {
  const tableWrapper = document.getElementById("tableWrapper");
  const tableBody = document.getElementById("milestoneTableBody");

  if (tableWrapper.style.display === "none") {
    tableWrapper.style.display = "block";
    tableBody.innerHTML = "";

    const departureDate = new Date(
      milestones.find((m) => m.name === "出發").date
    );

    // Filter and sort milestones: D-139 to D-0, sorted by date (latest to earliest)
    const filteredMilestones = milestones
      .map((m) => {
        const dCountdown = Math.round(
          (departureDate - new Date(m.date)) / (1000 * 60 * 60 * 24)
        );
        return { ...m, dCountdown };
      })
      .filter((m) => m.dCountdown >= 0 && m.dCountdown <= 139)
      .sort((a, b) => b.dCountdown - a.dCountdown); // Sort by D-day descending (D-139 to D-0)

    filteredMilestones.forEach((m) => {
      const row = document.createElement("tr");
      const nameCell = document.createElement("td");
      const dateCell = document.createElement("td");
      const countdownCell = document.createElement("td");

      nameCell.textContent = m.name;
      dateCell.textContent = m.date;
      countdownCell.textContent = `D-${m.dCountdown}`;

      // Highlight Today row
      if (m.name === "Today") {
        row.style.backgroundColor = "rgba(230, 57, 70, 0.1)";
        row.style.fontWeight = "600";
      }

      row.appendChild(nameCell);
      row.appendChild(dateCell);
      row.appendChild(countdownCell);
      tableBody.appendChild(row);
    });
  } else {
    tableWrapper.style.display = "none";
  }
}
