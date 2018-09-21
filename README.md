# updateHoldings
Project to update library holdings to vendor platforms

Steps of the project:

1. Create a Query Collection
2. Extract records with an ISBN (020 field)
3. Save MARC delivery as CSV File using MARC Edit.
	a. Export as tab (or comma) delimited values
	b. Export only 001, 020, 245 fields.
4. Make sure all eIsbn comments are in the appropriate file (EIsbnComments.txt)
	a. Copy EisbnComments to the folder.
	b. Copy 020 column in a new txt file
	c. Run code (UpdateHoldings_Comments_Clean.py)
	d. Remove all print comments and add those that are not already in EIsbnComments.txt
5. Deal with subscriptions if necessary:
	a. Upload MARC collections with subscriptions.
	b. Save as CSV using MARCEdit: LDR, 001, 245, 300
	c. Check LDR and 300 fields, to make sure they are all in code
		a. LDR: 8 position =  I (integrating resource) or m (monograph)
		b. 300: words = online, computer, electronic…
	d. Run subscription_clean.py
	e. Run UpdateHoldings_subscriptions_API.py
6. First phase of the code (UpdateHoldings_FirstPhase.py)
7. Take all ISBN from 1_FirstResults.csv
8. Search Gobi (Search all titles by ISBN).
9. Save results in gobi_list.csv
10. Second phase of the code (UpdateHoldings_SecondPhase.py)
11. Third phase of the code (ErrorHandling_ThirdPhase.py)
	a. Check all titles that don't match manually.
12. Find ISBN for errors printed in all error files.
13. Send all ISBN to GOBI


