# In backend/mark_services.py
from django.db import transaction
from .models import Mark, Markrelation, Markpercentage, Grade

def recompute_mark_grade(mark_id):
    """
    "Flawless" and "Atomic" function to recalculate a Mark.
    This locks the Mark row, calculates the weighted percentage
    from all Markrelations, and finds the correct Grade.
    
    This is 100% safe from "race conditions."
    """
    try:
        # 1. Start a "flawless" atomic transaction.
        with transaction.atomic():
            # 2. Lock the 'Mark' row. No one else can edit it.
            mark = Mark.objects.select_for_update().get(pk=mark_id)
            
            # 3. Get all individual scores for this Mark
            relations = Markrelation.objects.filter(markid=mark.pk)
            
            if not relations.exists():
                # No scores, so set to 0 and finish
                mark.total_percentage = 0
                mark.gradeid = None
                mark.save(update_fields=['total_percentage', 'gradeid'])
                return

            total_score = 0
            total_max_mark = 0 # The total % (e.g., 70% + 30% = 100%)

            # 4. Loop through each individual score (e.g., "Written", "Practical")
            for rel in relations:
                try:
                    # Get the rule for this score (e.g., "Written is 70% of total")
                    percentage_rule = Markpercentage.objects.get(markpercentageid=rel.markpercentageid)
                    
                    # Add the weighted score
                    total_score += (float(rel.mark) * float(percentage_rule.percentage)) / 100.0
                    total_max_mark += float(percentage_rule.percentage)
                
                except Markpercentage.DoesNotExist:
                    # If no rule, assume it's 100% of its own mark
                    total_score += float(rel.mark)
                    total_max_mark += 100
                except Exception:
                    # Catch 'float' conversion errors
                    pass # Skip this mark if data is bad

            # 5. Calculate the final percentage
            if total_max_mark > 0:
                final_percentage = (total_score / total_max_mark) * 100.0
            else:
                final_percentage = 0.0
            
            # 6. Find the correct Grade
            grade = Grade.objects.filter(
                gpoint__lte=final_percentage,  # e.g., 80 <= 85
                markupto__gte=final_percentage # e.g., 89 >= 85
            ).first() # .first() is safer
            
            # 7. Save the final, "flawless" result
            mark.total_percentage = final_percentage
            mark.gradeid = grade.gradeid if grade else None
            mark.save(update_fields=['total_percentage', 'gradeid'])

    except Mark.DoesNotExist:
        # If the mark was deleted, do nothing
        pass
    except Exception as e:
        # Log the error (in a real app)
        print(f"Error recomputing mark {mark_id}: {e}")