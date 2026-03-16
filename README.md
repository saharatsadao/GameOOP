# Eden of the Continuum

ยินดีต้อนรับสู่โปรเจกต์เกม **Eden of the Continuum** เกมแนว Action Platformer ที่พัฒนาด้วย Python และ Pygame โดยนำเสนอประสบการณ์การเล่นที่รวดเร็วและงานศิลป์สไตล์พรีเมียม

---

## รายละเอียดทีม
**ชื่อทีม:** ไม่สะอื้นอะ สดชื่นด้วยซ้ำ

### รายชื่อสมาชิก
1. **นายสหรัถ สะเดาว์** (68114540650)
2. **นางสาวรัชรินทร์ แสงภักดิ์** (68114540515)

---

## ฟีเจอร์เด่นของเกม (Key Features)

- **ตัวละครที่ได้รับแรงบันดาลใจจาก Sasuke:** ใช้ระบบ Sprite Factory ในการวาดตัวละครแบบ Real-time พร้อมชุดสีระดับพรีเมียมและการเคลื่อนไหวที่ลื่นไหล
- **ระบบศัตรูหลากหลายธีม:** 
  - **Halloween:** ผี (Ghost), ฟักทอง (Pumpkin), แมงมุม (Spider)
  - **Candy Land:** มนุษย์ขนมปังขิง (Gingerbread Man), สัตว์ประหลาดลูกอม (Candy Monster), ขนมบินได้ (Flying Sweet)
  - **Ocean:** ทากทะเล (Ocean Slug), ปู (Ocean Crab), ฉลาม (Shark)
  - **Urban:** พวกนักเลง (Urban Thug), โดรน (Urban Drone)
- **ระบบด่าน:** มีระบบปลดล็อกด่าน (Level Unlock) และการเลือกด่านผ่านหน้าจอ Level Select
- **เอฟเฟกต์ภาพ:** ระบบหน้าจอสั่น (Screen Shake), แสง God Rays ในด่านใต้ทะเล และฟองสบู่ (Bubbles)
- **ระบบเสียง:** เสียงประกอบและเสียงเอฟเฟกต์ (Jump, Stomp, Coin)

---

## การควบคุม (Controls)

| การกระทำ | ปุ่มกด |
| :--- | :--- |
| **เคลื่อนที่ซ้าย/ขวา** | `A` / `D` หรือ `Arrow Left` / `Arrow Right` |
| **กระโดด** | `Spacebar` / `W` / `Up` / `K` |
| **กลับหน้าเมนู** | `Esc` |
| **เลือกเมนู** | `Mouse Left Click` หรือ `Enter` |

---

## โครงสร้างทางเทคนิค (Technical Architecture)

โปรเจกต์นี้ถูกออกแบบโดยใช้หลักการ Object-Oriented Programming (OOP) และมีการแยกส่วนการทำงานที่ชัดเจน:
- **Engine:** จัดการ Loop หลักของเกม, การประมวลผลเหตุการณ์ (Events), และการวาดภาพ
- **State Management:** ควบคุมสถานะต่างๆ ของเกม (Menu, Level Select, Play, Game Over, Level Clear)
- **Sprite Factory:** ใช้ Pygame Draw ในการสร้าง Assets แบบ Dynamic เพื่อลดการใช้ไฟล์รูปภาพภายนอกและเพิ่มความยืดหยุ่นในการปรับแต่ง
- **World System:** จัดการการโหลดแผนที่จากข้อมูล List ใน Code (`level_data.py`) และการจัดการ Camera Scrolling

---

## วิธีการติดตั้ง

1. **เตรียมสภาพแวดล้อม:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # สำหรับ Windows
   ```

2. **ติดตั้ง Library:**
   ```bash
   pip install -r requirements.txt
   ```

## วิธีการใช้งาน

เริ่มเกมโดยการรันไฟล์ `main.py`:
```bash
python main.py
```
