## salary expense and saves

sal = 45989					## 35000 + 989

loan = 8200
bhisi = 10000
copart_adv_repay = 92000/8 	## copart_adv_repay >>> 11500.0

wifi = 1000
house_expense = 9000     ## grocery, electricity, rice-bag, cooking-oil.
miscellaneous = 1000 	 ## mobile recharge (mine + pappa) + 190 youtube premium + 75.0 hotstar

all_expenses = [loan, bhisi, copart_adv_repay, wifi, house_expense, miscellaneous]

def in_inr(amt):
	return f'{amt} Rs/-'

def calc_expenses():
	exp = sum(all_expenses)
	return exp


print("Balance with-out copart_adv_repay            ->", in_inr( sal-calc_expenses() + copart_adv_repay))
print("Balance after copart_adv_repay               ->", in_inr( sal-calc_expenses() ))

# print("Total expense with-out copart_adv_repay      ->", in_inr( sum(all_expenses) - copart_adv_repay ))
# print("Total expense with copart_adv_repay          ->", in_inr( sum(all_expenses) ))

print("\n"*3)

