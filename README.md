# updateHoldings
Project to update library holdings to vendor platforms

Steps of the project:/t
	1. Create a Query Collection
	2. Save MARC delivery as CSV File using MARC Edit.
		a. Export as tab (or comma) delimited values
		b. Export only 001, 020, 245 fields.
	3. First phase of the code
	4. Take all ISBN from printFirstPhase.txt
	5. Deal with errors accordingly.
	6. Find all unique OCN and save the OCN and the ISBN to uniqueIsbnFirstPhase.txt
	7. Batch Search vendor platform (Search all titles by ISBN)
	8. Save results
	9. Find all only print OCN
	10. Second phase of the code
	11. Send ISBN to GOBI (printSecondPhase.txt)
	12. Deal with errors accordingly (errorSecondPhase.txt)
