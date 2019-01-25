def open_file():
    filename = input("Input a file name: ")
    return open(filename, 'r')

def revenue(num_sales, sale_price): return num_sales * sale_price

def cost_of_goods_sold(num_ads, ad_price, num_sales, production_cost):
    return num_ads*ad_price + num_sales*production_cost

def calculate_ROI(placementCount, placementCost, salesNumber, productPrice, productionCost):
    costs = cost_of_goods_sold(placementCount, placementCost, salesNumber, productionCost)
    return (salesNumber * productPrice - costs) / costs

final_roi = 0
final_roi_who = ''

sales = 0
best_performing = ''

def updatePER(sale, ad):
    global sales, best_performing
    if sale > sales:
        sales = sale
        best_performing = ad

def updateROI(roi, ad):
    global final_roi, final_roi_who
    if roi > final_roi:
        final_roi = roi
        final_roi_who = ad

def main():
    global sales, best_performing
    global final_roi, final_roi_who
    fp = open_file()
    print()
    print("RobCo AdStats M4000")
    print("-------------------")

    state = 0
    current = ""
    #for each line of file
    for line in fp:
        line = line.strip()
        if line:
            product = line[:27].strip()
            ad = line[27:58].strip()
            placement_count = int(line[58:62].strip())
            placement_cost = float(line[62:70].strip())
            sales_number = int(line[70:78].strip())
            product_price = float(line[78:86].strip())
            production_cost = float(line[86:].strip())

            total_revenue = revenue(sales_number, product_price)#calculate revenue
            roi = calculate_ROI(placement_count, placement_cost, sales_number, product_price, production_cost)#calculate ROI

            if product != current and state != 0:
                state = 3
            if state == 0:
                updatePER(sales_number, ad)
                updateROI(roi, ad)
                state = 1
                current = product

            if state == 1 and current == product:
                updatePER(sales_number, ad)
                #find the maximum value of ROI, and record its ad name
                updateROI(roi, ad)
                current = product
            else:

                print("\n" + current)
                print("  {:27s}{:>11s}".format("Best-Performing Ad", "sales"))
                print("  {:27s}{:>11d}".format(best_performing, sales))
                print("\n  {:27s}{:>11s}".format("Best ROI", "percent"))
                print("  {:27s}{:>10.2f}%".format(final_roi_who, final_roi))
                #reset the record
                best_performing = ""
                sales = 0
                final_roi = 0.0
                final_roi_who = ""
                state = 1
                current = product

                updatePER(sales_number, ad)
                updateROI(roi, ad)

    print("\n" + current)
    print("  {:27s}{:>11s}".format("Best-Performing Ad", "sales"))
    print("  {:27s}{:>11d}".format(best_performing, sales))
    print("\n  {:27s}{:>11s}".format("Best ROI", "percent"))
    print("  {:27s}{:>10.2f}%".format(final_roi_who, final_roi))
    print()


if __name__ == '__main__':
    main()