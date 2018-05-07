# updateHoldings
Project to update library holdings to vendor platforms

Steps of the project:

1. Create a Query Collection
2. Extract records with an ISBN (020 field)
3. Save as CSV File using MarcEdit.
	a. Export 001, 020, 245 fields  as tab (or comma) delimited values
4. Make sure all eIsbn comments are in the file.       
5. If necessary, update the subscriptions list:
	a. Upload MARC collections
	b. Save as CSV: LDR, 001, 245, 300
	c. Run subscription_clean.py
6. Run API code of all subscriptions to remove the ones also found as a perpetual title.
7. First phase of the code (gobi_FirstPhase.py) : Clean and select certain ISBNs
8. Take all selected ISBN (1_FirstPhase.txt)
9. Batch Search Gobi (Search all titles by ISBN)
10. Second phase of the code (gobi_SecondPhase.py) : Select only electronic books and match the titles.
11. Third phase of the code (errorHandling.py)
12. Manually find ISBN for all errors (found in error files)
13. Send all ISBN to GOBI

