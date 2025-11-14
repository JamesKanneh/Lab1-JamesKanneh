#!/usr/bin/env python3
"""
grade-generator.py
ALU Individual Coding Lab - Grade generator that enforces FA=60 / SA=40 limits,
prints ALU-style summary and writes grades.csv.
"""

import csv

FA_LIMIT = 60.0
SA_LIMIT = 40.0

class Assignment:
    def __init__(self, name, category, grade, weight):
        self.name = name
        self.category = category.upper()
        self.grade = float(grade)
        self.weight = float(weight)

    def weighted_grade(self):
        return (self.grade / 100.0) * self.weight

def is_valid_category(cat):
    return cat.upper() in ("FA", "SA")

def get_float(prompt):
    while True:
        val = input(prompt).strip()
        try:
            f = float(val)
            return f
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("\n--- Student Grade Generator (ALU) ---\n")

    assignments = []
    total_fa_weight = 0.0
    total_sa_weight = 0.0

    while True:
        name = input("Enter Assignment Name: ").strip()
        while not name:
            print("Assignment name cannot be empty.")
            name = input("Enter Assignment Name: ").strip()

        category = input("Enter Category (FA or SA): ").strip().upper()
        while not is_valid_category(category):
            print("Invalid category. Enter FA or SA.")
            category = input("Enter Category (FA or SA): ").strip().upper()

        # get grade
        grade = get_float("Enter Grade (0-100): ")
        while grade < 0 or grade > 100:
            print("Grade must be between 0 and 100.")
            grade = get_float("Enter Grade (0-100): ")

        # get weight, validate positive and not exceed category remaining quota
        weight = get_float("Enter Weight (positive number): ")
        while weight <= 0:
            print("Weight must be a positive number.")
            weight = get_float("Enter Weight (positive number): ")

        # check remaining quota
        if category == "FA":
            if total_fa_weight + weight > FA_LIMIT + 1e-9:
                remaining = FA_LIMIT - total_fa_weight
                print(f"Cannot add weight: that would exceed FA limit of {FA_LIMIT}.")
                print(f"Remaining FA quota: {remaining:.2f}. Try a smaller weight.")
                continue
            total_fa_weight += weight
        else:  # SA
            if total_sa_weight + weight > SA_LIMIT + 1e-9:
                remaining = SA_LIMIT - total_sa_weight
                print(f"Cannot add weight: that would exceed SA limit of {SA_LIMIT}.")
                print(f"Remaining SA quota: {remaining:.2f}. Try a smaller weight.")
                continue
            total_sa_weight += weight

        assignments.append(Assignment(name, category, grade, weight))

        more = input("Add another assignment? (y/n): ").strip().lower()
        if more != 'y':
            break

    # Calculations
    total_fa = sum(a.weighted_grade() for a in assignments if a.category == "FA")
    total_sa = sum(a.weighted_grade() for a in assignments if a.category == "SA")
    total_grade = total_fa + total_sa
    gpa = (total_grade / 100.0) * 5.0

    # Determine pass/fail: must score >=50% of each category's total weight
    required_fa = FA_LIMIT * 0.5  # i.e., 50% of FA limit (30 if FA_LIMIT=60)
    required_sa = SA_LIMIT * 0.5  # i.e., 50% of SA limit (20 if SA_LIMIT=40)
    pass_fa = total_fa >= required_fa - 1e-9
    pass_sa = total_sa >= required_sa - 1e-9
    status = "PASSED" if (pass_fa and pass_sa) else "FAILED"

    # ALU-style Console Summary (matches screenshot)
    print("\n--- RESULTS ---")
    print(f"Total Formative: {total_fa:.2f} / {FA_LIMIT:.0f}")
    print(f"Total Summative: {total_sa:.2f} / {SA_LIMIT:.0f}")
    print("****************")
    print(f"Total Grade: {total_grade:.2f} / 100")
    print(f"GPA: {gpa:.4f}")
    print(f"Status: {status}")

    # Write grades.csv
    with open("grades.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Assignment", "Category", "Grade", "Weight"])
        for a in assignments:
            writer.writerow([a.name, a.category, f"{a.grade:.0f}" if a.grade.is_integer() else a.grade, a.weight])

    print("\ngrades.csv created with all assignments.")

if __name__ == "__main__":
    main()