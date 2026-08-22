# Bulk Upload Guide — College & Exam

Admin: https://portal.admissionsbazaar.com/admin/

## Pehle ek baar

```bash
python manage.py seed_masters
python manage.py export_bulk_templates
```

Templates folder: `media/import_templates/`

- `college_bulk_template.xlsx`
- `exam_bulk_template.xlsx`
- `upcoming_exam_bulk_template.xlsx`

Har file me sheet **HOW_TO_FILL** bhi hai.

---

## College import (step by step)

1. Template download / generate karo.
2. **Data** sheet me rows bhara — **header mat badlo**.
3. Har college ke liye **alag** `college_user` email:
   - Example: `amaltas.college@admissionsbazaar.com`
4. Naya email ho to `user_name` + `user_mobile` bharo (auto College User banega).
5. `organization_type`: `Private` / `Government`
6. `college_type`: `Medical` / `Engineering` / …
7. `rank`: unique number (e.g. 101, 102)
8. Admin → **Colleges** → **Import** → file choose → Confirm

### Required columns

`college_user, name, organization_type, college_type, rank, established_year, overview, city`

### Optional

`user_name, user_mobile, user_password, affiliation, rating, course_categories, primary_mobile, email, website, meta_title, slug`

`course_categories` example: `Medical|Engineering`

### Aapka pehle wala error

`CollegeAdmin matching query does not exist`  
Matlab Excel me `college_user` email DB me College User nahi tha.

Ab naya email + `user_name`/`user_mobile` se **auto-create** ho jayega.  
Purane export file mat reuse karo agar columns gadbad hain — **naya template** use karo.

---

## Exam import

1. `exam_bulk_template.xlsx` bhara
2. Admin → **Exams** → **Import**
3. `course_category` exact master name

## Upcoming Exam import

1. Pehle Exam exist kare
2. `upcoming_exam_bulk_template.xlsx` — column `exam` = Exam title
3. Dates: `YYYY-MM-DD`
4. Admin → **Upcoming Exams** → **Import**

---

## Common problems

| Error | Fix |
|-------|-----|
| College User not found | `user_name`+`user_mobile` do, ya pehle College Users me banao |
| already linked to college | Us email pe pehle se college hai — naya email use karo |
| organization_type not found | Exact `Private` / `Government` + `seed_masters` |
| rank duplicate | Alag rank number |
| date error | `2026-05-03` format |

Logo/image Excel se nahi aate — import pe placeholder auto lagta hai; baad me admin se change karo.
