//
//  ContentView.swift
//  MediMate
//
//  Created by Simon Bestler on 09.05.25.
//

import SwiftUI
import SwiftData
import HealthKit

// Add HealthKitManager as an observable object
@MainActor
class ContentViewModel: ObservableObject {
    @Published var isAuthorized = false
    @Published var stepCount: Double = 0.0
    let healthKitManager = HealthKitManager()

    func requestHealthKit() {
        healthKitManager.requestAuthorization { [weak self] success in
            DispatchQueue.main.async {
                self?.isAuthorized = success
                if success {
                    self?.fetchSteps()
                }
            }
        }
    }

    func fetchSteps() {
        healthKitManager.fetchStepCount()
        self.stepCount = healthKitManager.stepCount
    }
}


struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var items: [Item]
    @StateObject private var viewModel = ContentViewModel()

    var body: some View {
        NavigationSplitView {
            List {
                ForEach(items) { item in
                    NavigationLink {
                        Text("Item at \(item.timestamp, format: Date.FormatStyle(date: .numeric, time: .standard))")
                    } label: {
                        Text(item.timestamp, format: Date.FormatStyle(date: .numeric, time: .standard))
                    }
                }
                .onDelete(perform: deleteItems)
            }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    EditButton()
                }
                ToolbarItem {
                    Button(action: addItem) {
                        Label("Add Item", systemImage: "plus")
                    }
                }
            }
            Section(header: Text("Apple HealthKit Integration")) {
                if viewModel.isAuthorized {
                    VStack {
                        Text("Today's Step Count: \(viewModel.healthKitManager.stepCount, specifier: "%.0f")")
                        Button("Refresh Steps") {
                            viewModel.fetchSteps()
                        }
                    }
                } else {
                    Button("Connect to Apple HealthKit") {
                        viewModel.requestHealthKit()
                    }
                }
            }
        } detail: {
            Text("Select an item")
        }
    }

    private func addItem() {
        withAnimation {
            let newItem = Item(timestamp: Date())
            modelContext.insert(newItem)
        }
    }

    private func deleteItems(offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(items[index])
            }
        }
    }
}

#Preview {
    ContentView()
        .modelContainer(for: Item.self, inMemory: true)
}
