
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { parse, isValid, format  } from "date-fns";

interface Vaccination {
  name: string;
  doctor: string;
  date: string;
}

interface VaccinationsCardProps {
  vaccinations: Vaccination[];
}

function parseFlexibleDate(input: string): Date | null {
  const formats = ['dd.MM.yyyy', 'MM/yyyy', 'yyyy-MM-dd'];

  for (const fmt of formats) {
    const parsed = parse(input, fmt, new Date());
    if (isValid(parsed)) return parsed;
  }

  return null;
}

export default function VaccinationsCard({ vaccinations }: VaccinationsCardProps) {
  return (
    <Card className="shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg text-medical-primary">Vaccinations</CardTitle>
      </CardHeader>
      <CardContent>
        {vaccinations.length === 0 ? (
          <p className="text-sm text-gray-500">No vaccination records found</p>
        ) : (
          <div className="space-y-2">
            {vaccinations.map((vax, index) => {
              const parsedDate = parseFlexibleDate(vax.date);
              return (
                <div key={index} className="border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                  <div className="flex justify-between items-start">
                    <h3 className="font-medium text-medical-text">{vax.name}</h3>
                    <span className="text-sm text-gray-500">
                      {parsedDate ? format(parsedDate, "MMM d, yyyy") : "Invalid date"}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{vax.doctor}</p>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
