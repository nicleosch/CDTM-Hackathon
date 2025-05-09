// HealthKitManager.swift
// MediMate
//
// Created for Apple HealthKit integration

import Foundation
import HealthKit

class HealthKitManager: ObservableObject {
    private let healthStore = HKHealthStore()
    @Published var stepCount: Double = 0.0
    
    func requestAuthorization(completion: @escaping (Bool) -> Void) {
        guard HKHealthStore.isHealthDataAvailable() else {
            completion(false)
            return
        }
        let stepType = HKQuantityType.quantityType(forIdentifier: .stepCount)!
        let typesToRead: Set = [stepType]
        healthStore.requestAuthorization(toShare: [], read: typesToRead) { success, _ in
            completion(success)
        }
    }
    
    func fetchStepCount() {
        let stepType = HKQuantityType.quantityType(forIdentifier: .stepCount)!
        let now = Date()
        let startOfDay = Calendar.current.startOfDay(for: now)
        let predicate = HKQuery.predicateForSamples(withStart: startOfDay, end: now, options: .strictStartDate)
        let query = HKStatisticsQuery(quantityType: stepType, quantitySamplePredicate: predicate, options: .cumulativeSum) { [weak self] _, result, _ in
            guard let self = self else { return }
            DispatchQueue.main.async {
                if let sum = result?.sumQuantity() {
                    self.stepCount = sum.doubleValue(for: HKUnit.count())
                } else {
                    self.stepCount = 0.0
                }
            }
        }
        healthStore.execute(query)
    }
}
