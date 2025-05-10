
import { Card, CardContent } from "@/components/ui/card";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";

interface PatientHeaderProps {
  patientData: {
    name: string;
    dateOfBirth: string;
    gender: string;
    address: string;
    insurance: {
      provider: string;
      insuranceNumber: string;
    };
  };
  reasonForVisit: string;
}

export default function PatientHeader({ patientData, reasonForVisit }: PatientHeaderProps) {
  // Calculate age from date of birth
  const calculateAge = (dob: string) => {
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  };

  const age = calculateAge(patientData.dateOfBirth);

  return (
    <Card className="shadow-sm border-medical-secondary/30">
      <CardContent className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <div className="flex flex-col space-y-2">
              <div className="flex items-baseline">
                <h2 className="text-2xl font-bold text-medical-text mr-2">{patientData.name}</h2>
                <span className="text-sm text-gray-500">{patientData.gender}, {age} years</span>
              </div>
              
              <div className="flex items-center text-sm text-gray-500">
                <CalendarIcon className="h-4 w-4 mr-1" />
                <span>DOB: {format(new Date(patientData.dateOfBirth), "MMMM d, yyyy")}</span>
              </div>
              
              <div className="text-sm text-gray-500 mt-1">{patientData.address}</div>
              
              <div className="mt-3 pt-3 border-t border-gray-100">
                <div className="text-sm font-medium text-medical-primary">Insurance</div>
                <div className="text-sm text-gray-600">{patientData.insurance.provider}</div>
                <div className="text-sm text-gray-500">#{patientData.insurance.insuranceNumber}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-medical-primary/5 p-4 rounded-md">
            <h3 className="font-medium text-medical-primary mb-2">Reason for Visit</h3>
            <p className="text-sm text-gray-700">{reasonForVisit}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
