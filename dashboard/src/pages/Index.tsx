
import DashboardLayout from "@/components/DashboardLayout";
import PatientHeader from "@/components/PatientHeader";
import VitalsCard from "@/components/VitalsCard";
import ActivityChart from "@/components/ActivityChart";
import HealthMetricsCard from "@/components/HealthMetricsCard";
import MedicationsCard from "@/components/MedicationsCard";
import WellbeingCard from "@/components/WellbeingCard";
import SymptomsCard from "@/components/SymptomsCard";
import VaccinationsCard from "@/components/VaccinationsCard";
import { patientData } from "@/data/patientData";

const Index = () => {
  return (
    <DashboardLayout patientName={patientData.generalInformation.name} data={patientData}>
      <div className="space-y-6">
        {/* Patient Information */}
        <PatientHeader 
          patientData={patientData.generalInformation} 
          reasonForVisit={patientData.reasonsForVisit} 
        />
        
        {/* Vitals Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <VitalsCard 
            vitals={patientData.appleHealth.vitals} 
            respiratory={patientData.appleHealth.respiratory} 
            heart={patientData.appleHealth.heart} 
          />
          <ActivityChart activity={patientData.appleHealth.activity} />
        </div>
        
        {/* Health Metrics & Medications */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <HealthMetricsCard 
            bodyMeasurements={patientData.appleHealth.bodyMeasurements} 
            bloodGlucose={patientData.appleHealth.vitals.bloodGlucose} 
          />
          <MedicationsCard medications={patientData.appleHealth.medications} />
        </div>
        
        {/* Wellbeing & Symptoms */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <WellbeingCard 
            mentalWellbeing={patientData.appleHealth.mentalWellbeing} 
            sleep={patientData.appleHealth.sleep} 
          />
          <div className="space-y-6">
            <SymptomsCard symptoms={patientData.appleHealth.symptoms} />
            <VaccinationsCard vaccinations={patientData.vaccinations} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Index;
