from cleansweep.models import db
from cleansweep.stats import Stats, register_stats

@register_stats
class BoothCoverage(Stats):
    NAME = "BoothCoverage"
    TYPE = "number"
    TITLE = "Booth Coverage"
    MESSAGE = "#booths with at least one volunteer"
    cummulative = True

    def get_timeseries_data(self, place):
        raise NotImplementedError()

    def get_total(self, place):
        q = """
            SELECT count(*) FROM (
                SELECT place.name, count(*) 
                FROM place, place_type, place_parents p
                WHERE place.type_id=place_type.id
                  AND place_type.short_name='PB' 
                  AND place.id=p.child_id
                  AND p.parent_id=%s
                GROUP BY place.name) as t
            """
        result = db.engine.execute(q, [place.id]).fetchone()
        return result[0]
