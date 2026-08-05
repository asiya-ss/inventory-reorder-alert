import csv
inventory=[]
restock_items=[]
with open("inventory.csv","r") as file:
    reader=csv.DictReader(file)
    for row in reader:
        try:
            item=row["Item"]
            quantity=int(row["Quantity"])
            threshold=int(row["Threshold"])

            inventory.append({
                "item":item,
                "quantity": quantity,
                "threshold": threshold
            })
        except (ValueError, KeyError):
            print("Skipping invalid row.")

print("\nRESTOCK REPORT")
print("-" * 50)
print(f"{'Item':<25} {'Qty':<5} {'Threshold':<12} {'Status':<12}")
print("-" * 50)
for item in inventory:
    if item["quantity"]<item["threshold"]:
        difference=item["threshold"]-item["quantity"]
        if item["quantity"]<item["threshold"]*0.25:
            priority="CRITICAL"
        else:
            priority="LOW"
        print(
        f"{item['item']}| Qty:{item['quantity']}|"
        f"{priority} | "
        f"Threshold: {item['threshold']} | "
        f"Need to reorder {difference}"
    )

        restock_items.append({
    "Item":item["item"],
    "Quantity":item["quantity"],
    "Threshold": item["threshold"],
    "Reorder Qty": difference
      }) 
    else:
        print(
            f"{item['item']} | QTy:{item['quantity']} | "
            f"Threshold: {item['threshold']} | "
            f"IN STOCK"
        )
if len(restock_items) == 0:
    print("Everything is sufficiently stocked.")


with open("restock_report.csv","w",newline="") as file:
    fieldnames = [
        "Item",
        "Quantity",
        "Threshold",
        "Reorder Qty"
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(restock_items)

print("\nCSV report generated successfully!")



print("\n" + "=" * 40)
print("SIMULATED EMAIL ALERT")
print("=" * 40)
print("Subject: Inventory Restock Alert\n")

if restock_items:
    print("Dear Inventory Manager,\n")
    print("The following items require restocking:\n")

    for item in restock_items:
        print(f"-{item['Item']}:Reorder {item['Reorder Qty']} units")
    print("\nPlease arrange the purchase of these items as soon as possible.")
    print("\nRegards,")
    print("Inventory Monitoring System")
else:
    print("Dear Inventory Manager,\n")
    print("All inventory items are sufficiently stocked.")
    print("\nRegards,")
    print("Inventory Monitoring System")    