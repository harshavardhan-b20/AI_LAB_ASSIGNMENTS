# 📋 Software Requirements Specification (SRS)
# Gladiator - Employee Resource Management App

**Version:** 1.0  
**Date:** March 11, 2026  
**Technology Stack:** Android (Kotlin) + Jetpack Compose + Firebase Realtime Database  
**Architecture:** MVVM (Model-View-ViewModel)

---

## 📑 Table of Contents

1. [Introduction](#1-introduction)
2. [User Roles & Permissions](#2-user-roles--permissions)
3. [MVVM Architecture](#3-mvvm-architecture)
4. [Folder Structure](#4-folder-structure)
5. [Firebase Database Structure](#5-firebase-database-structure)
6. [Entity Relationship Diagram](#6-entity-relationship-diagram)
7. [User Flow Diagrams](#7-user-flow-diagrams)
8. [Data Models (Kotlin)](#8-data-models-kotlin)
9. [Firebase Security Rules](#9-firebase-security-rules)
10. [Screen Access Control](#10-screen-access-control)
11. [UI Components](#11-ui-components)
12. [Summary](#12-summary)

---

## 1. Introduction

### 1.1 Purpose
Gladiator is an Android application designed to manage employee resources within an organization. It connects **Project Managers** who need skilled employees with **Employees** who are available (on bench) for new projects.

### 1.2 Scope
- Employee profile management with skills and availability
- Project posting by Project Managers
- Employee bench status tracking
- Project application system
- Skill-based employee search

### 1.3 Key Features
- **For Employees:** Manage profile, toggle bench status, view & apply to projects
- **For Project Managers:** Post projects, search benched employees, manage applications

---

## 2. User Roles & Permissions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER ROLES                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│    ┌────────��────────────────┐         ┌─────────────────────────┐          │
│    │      👔 EMPLOYEE        │         │   👨‍💼 PROJECT MANAGER    │          │
│    ├─────────────────────────┤         ├─────────────────────────┤          │
│    │ ✅ Create Account       │         │ ✅ Create Account       │          │
│    │ ✅ Edit Profile         │         │ ✅ Edit Profile         │          │
│    │ ✅ Add Skills           │         │ ✅ Upload Projects      │          │
│    │ ✅ Set Bench Status     │         │ ✅ Edit/Delete Projects │          │
│    │ ✅ View Projects        │         │ ✅ Search Employees     │          │
│    │ ✅ Apply to Projects    │         │ ✅ View Applications    │          │
│    │ ❌ Cannot Post Projects │         │ ✅ Accept/Reject Apps   │          │
│    └─────────────────────────┘         └─────────────────────────┘          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Employee Permissions
| Permission | Allowed |
|------------|---------|
| Create Account | ✅ |
| Edit Own Profile | ✅ |
| Add/Update Skills | ✅ |
| Toggle Bench Status | ✅ |
| View All Projects | ✅ |
| Apply to Projects | ✅ |
| Upload/Post Projects | ❌ |
| Search Employees | ❌ |
| Accept/Reject Applications | ❌ |

### 2.2 Project Manager Permissions
| Permission | Allowed |
|------------|---------|
| Create Account | ✅ |
| Edit Own Profile | ✅ |
| Upload/Post Projects | ✅ |
| Edit/Delete Own Projects | ✅ |
| View All Projects | ✅ |
| Search Employees | ✅ |
| Filter by Bench Status | ✅ |
| View Applications | ✅ |
| Accept/Reject Applications | ✅ |
| Toggle Bench Status | ❌ |
| Apply to Projects | ❌ |

---

## 3. MVVM Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MVVM ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────────┐    │
│  │     VIEW     │ ◄─────► │  VIEWMODEL   │ ◄─────► │    REPOSITORY    │    │
│  │  (Composable)│         │ (StateFlow)  │         │  (Data Source)   │    │
│  └──────────────┘         └──────────────┘         └────────┬─────────┘    │
│         │                        │                           │              │
│         │ Observes               │ Exposes                   │ Fetches     │
���         │ UI State               │ State &                   │ Data        │
│         │                        │ Events                    │              │
│         ▼                        ▼                           ▼              │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────────┐    │
│  │   Screens    │         │  UI State    │         │     Firebase     │    │
│  │  Components  │         │  Data Class  │         │ Realtime Database│    │
│  │   Buttons    │         │   LiveData   │         │ Authentication   │    │
│  └──────────────┘         └──────────────┘         └──────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Data Flow

```
  USER ACTION          UI LAYER              VIEWMODEL            REPOSITORY
      │                   │                      │                    │
      │   Click Button    │                      │                    │
      ├──────────────────►│                      │                    │
      │                   │  Call ViewModel      │                    │
      │                   │     Function         │                    │
      │                   ├─────────────────────►│                    │
      │                   │                      │  Call Repository   │
      │                   │                      ├───────────────────►│
      │                   │                      │                    │
      │                   │                      │                    │  Firebase
      │                   │                      │                    │  Realtime
      │                   │                      │                    │  Database
      │                   │                      │                    ├─────────►
      │                   │                      │                    │
      │                   │                      │                    │◄─────────
      │                   │                      │  Return Result     │
      │                   │                      │◄───────────────────┤
      │                   │  Update UI State     │                    │
      │                   │◄─────────────────────┤                    │
      │   UI Updated      │                      │                    │
      │◄──────────────────┤                      │                    │
```

---

## 4. Folder Structure

```
📦 app/src/main/java/com/example/gladiator/
│
├── 📄 MainActivity.kt                 # Entry point, Navigation Host
├── 📄 GladiatorApp.kt                 # Application class (for DI)
│
├── 📁 data/                           # ═══════ DATA LAYER ═══════
│   │
│   ├── 📁 model/                      # Data Models (POJOs/Data Classes)
│   │   ├── 📄 User.kt                 # Basic user authentication data
│   │   ├── 📄 Profile.kt              # Employee profile + bench status
│   │   ├── 📄 UserRole.kt             # Role enum (employee/project_manager)
│   │   ├── 📄 Project.kt              # Project requirements (PM creates)
│   │   ├── 📄 Application.kt          # Employee job applications
│   │   └── 📄 Skill.kt                # Skills master data
│   │
│   ├── 📁 repository/                 # Repository Pattern
│   │   ├── 📄 AuthRepository.kt       # Firebase Auth operations
│   │   ├── 📄 UserRepository.kt       # User CRUD operations
│   │   ├── 📄 ProfileRepository.kt    # Profile CRUD + bench status
│   │   ├── 📄 ProjectRepository.kt    # Project CRUD (PM only writes)
│   │   └── 📄 ApplicationRepository.kt # Application handling
│   │
│   └── 📁 firebase/                   # Firebase Services
│       ├── 📄 FirebaseService.kt      # Firebase Realtime DB helper
│       └── 📄 FirebaseAuthService.kt  # Firebase Auth helper
│
├── 📁 di/                             # ═══════ DEPENDENCY INJECTION ═══════
│   ├── 📄 AppModule.kt                # Hilt/Koin modules
│   └── 📄 RepositoryModule.kt         # Repository bindings
│
├── 📁 viewmodel/                      # ═══════ VIEWMODEL LAYER ═══════
│   ├── 📄 AuthViewModel.kt            # Handles Login/Signup state
│   ├── 📄 ProfileViewModel.kt         # Profile + bench status management
│   ├── 📄 ProjectViewModel.kt         # Project posting (PM only)
│   ├── 📄 SearchViewModel.kt          # Employee search
│   └── 📄 ApplicationViewModel.kt     # Application management
│
├── 📁 ui/                             # ═══════ UI LAYER (VIEW) ═══════
│   │
│   ├── 📁 auth/                       # Authentication Screens
│   │   ├── 📄 LoginScreen.kt          # Login UI
│   │   └── 📄 SignupScreen.kt         # Signup UI (role selection)
│   │
│   ├── 📁 employee/                   # Employee-Only Screens
│   │   ├── 📄 EmployeeDashboard.kt    # Employee home screen
│   │   ├── 📄 EmployeeProfileScreen.kt # Profile editing + bench toggle
│   │   ├── 📄 ViewProjectsScreen.kt   # Browse available projects
│   │   ├── 📄 ApplyProjectScreen.kt   # Apply to a project
│   │   └── 📄 MyApplicationsScreen.kt # Track application status
│   │
│   ├── 📁 manager/                    # Project Manager-Only Screens
│   │   ├── 📄 ManagerDashboard.kt     # PM home screen
│   │   ├── 📄 UploadProjectScreen.kt  # Create new project (PM ONLY)
│   │   ├── 📄 EditProjectScreen.kt    # Edit existing project
│   │   ├── 📄 MyProjectsScreen.kt     # PM's posted projects
│   │   ├── 📄 SearchEmployeeScreen.kt # Search employees by skills
│   │   └── 📄 ViewApplicationsScreen.kt # Accept/Reject applications
│   │
│   ├── 📁 components/                 # Reusable UI Components
│   │   ├── 📄 BenchStatusToggle.kt    # Bench toggle switch component
│   │   ├── 📄 ProjectCard.kt          # Project display card
│   │   ├── 📄 EmployeeCard.kt         # Employee display card
│   │   ├── 📄 SkillChips.kt           # Skill tag chips
│   │   ├── 📄 LoadingIndicator.kt     # Loading spinner
│   │   ├── 📄 ErrorDialog.kt          # Error popup
│   │   └── 📄 CommonComponents.kt     # Buttons, TextFields, etc.
│   │
│   ├── 📁 navigation/                 # Navigation Setup
│   │   ├── 📄 NavGraph.kt             # Navigation graph definition
│   │   ├── 📄 Routes.kt               # Route constants/sealed class
│   │   └── 📄 NavActions.kt           # Navigation helper functions
│   │
│   └── 📁 theme/                      # Theming
│       ├── 📄 Color.kt                # Color definitions
│       ├── 📄 Theme.kt                # Material theme setup
│       ├── 📄 Type.kt                 # Typography
│       └── 📄 Shape.kt                # Shape definitions
│
└── 📁 util/                           # ═══════ UTILITIES ═══════
    ├── 📄 Constants.kt                # App-wide constants
    ├── 📄 Resource.kt                 # Result wrapper (Success/Error/Loading)
    ├── 📄 Extensions.kt               # Kotlin extension functions
    └── 📄 Validators.kt               # Input validation helpers
```

---

## 5. Firebase Database Structure

```
📦 gladiator-db (Firebase Realtime Database Root)
│
│
├── 📁 users/                                    # USER AUTHENTICATION DATA
│   │
│   └── 📁 {userId}/
│       │
│       ├── uid: "firebase_auth_uid_123"
│       ├── email: "john.doe@company.com"
│       ├── fullName: "John Doe"
│       ├── role: "employee"                     # "employee" | "project_manager"
│       └── createdAt: 1710000000000             # Timestamp
│
│
├── 📁 profiles/                                 # EMPLOYEE PROFILES (Only for employees)
│   │
│   └── 📁 {userId}/
│       │
│       ├── uid: "firebase_auth_uid_123"
│       ├── experience: "5 years"
│       ├── location: "New York, USA"
│       ├── skills: [                            # Array of skills
│       │     "Kotlin",
│       │     "Android",
│       │     "Jetpack Compose",
│       │     "Firebase"
│       │   ]
│       ├── projectHistory: [                    # Past projects
│       │     "E-Commerce App",
│       │     "Banking App"
│       │   ]
│       ├── certifications: [                    # Certifications
│       │     "AWS Certified Developer",
│       │     "Google Cloud Professional"
│       │   ]
│       │
│       ├── ╔═══════════════════════════════════╗
│       │   ║        BENCH STATUS FIELDS        ║
│       │   ╚═══════════════════════════════════╝
│       ├── isBenched: true                      # TRUE = Available, FALSE = Working
│       ├── benchedSince: 1710000000000          # When employee became benched
│       │
│       ├── profileImageUrl: "https://..."
│       └── updatedAt: 1710000000000
│
│
├── 📁 projects/                                 # PROJECTS (PM ONLY CAN WRITE)
│   │
│   └── 📁 {projectId}/
│       │
│       ├── projectId: "proj_abc123"
│       ├── title: "E-Commerce Mobile App"
│       ├── description: "Build a complete shopping app with payment integration..."
│       │
│       ├── ╔═══════════════════════════════════╗
│       │   ║    PROJECT MANAGER (OWNER)        ║
│       │   ╚═══════════════════════════════════╝
│       ├── managerId: "pm_user_id_456"          # PM who created this project
│       ├── managerName: "Jane Smith"
│       │
│       ├── requiredSkills: [                    # Skills needed
│       │     "Kotlin",
│       │     "Jetpack Compose",
│       │     "REST API"
│       │   ]
│       ├── experienceRequired: "3+ years"
│       ├── teamSize: 5
│       ├── location: "Remote"
│       ├── startDate: 1710000000000
│       ├── endDate: 1720000000000
│       ├── status: "open"                       # "open" | "in_progress" | "closed"
│       └── createdAt: 1710000000000
│
│
├── 📁 applications/                             # EMPLOYEE APPLICATIONS
│   │
│   └── 📁 {applicationId}/
│       │
│       ├── applicationId: "app_xyz789"
│       ├── projectId: "proj_abc123"             # Which project
│       ├── employeeId: "emp_user_id_123"        # Who applied
│       ├── employeeName: "John Doe"
│       ├── employeeSkills: [                    # Applicant's skills
│       │     "Kotlin",
│       │     "Android"
│       │   ]
│       ├── status: "pending"                    # "pending" | "accepted" | "rejected"
│       ├── appliedAt: 1710000000000
│       ├── reviewedBy: "pm_user_id_456"         # PM who reviewed
│       └── reviewedAt: 1710500000000
│
│
└── 📁 skills/                                   # MASTER SKILLS LIST
    │
    └── 📁 {skillId}/
        │
        ├── skillId: "skill_001"
        ├── name: "Kotlin"
        └── category: "Programming Language"
```

---

## 6. Entity Relationship Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE RELATIONSHIPS                                │
└──────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │      USERS      │
                              ├─────────────────┤
                              │ uid (PK)        │
                              │ email           │
                              │ fullName        │
                              │ role ───────────┼──► "employee" OR "project_manager"
                              │ createdAt       │
                              └────────┬────────┘
                                       │
                 ┌─��───────────────────┴─────────────────────┐
                 │                                           │
                 │ if role = "employee"                      │ if role = "project_manager"
                 ▼                                           ▼
       ┌─────────────────┐                         ┌─────────────────┐
       │    PROFILES     │                         │    PROJECTS     │
       ├─────────────────┤                         ├─────────────────┤
       │ uid (FK) ────��──┼── References USERS      │ projectId (PK)  │
       │ experience      │                         │ title           │
       │ location        │                         │ description     │
       │ skills[]        │                         │ managerId (FK)──┼── References USERS
       │ projectHistory[]│                         │ managerName     │
       │ certifications[]│                         │ requiredSkills[]│
       │                 │                         │ teamSize        │
       │ ╔═════════════╗ │                         │ status          │
       │ ║ isBenched   ║◄┼── Employee toggles      │ startDate       │
       │ ║ benchedSince║ │                         │ endDate         │
       │ ╚═════════════╝ │                         │ createdAt       │
       │                 │                         └────────┬────────┘
       │ profileImageUrl │                                  │
       │ updatedAt       │                                  │ 1:N (One project, many apps)
       └────────┬────────┘                                  │
                │                                           │
                │ 1:N (One employee, many apps)             │
                │                                           │
                └─────────────────┬─────────────────────────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │  APPLICATIONS   │
                        ├─────────────────┤
                        │ applicationId   │ (PK)
                        │ projectId (FK)──┼── References PROJECTS
                        │ employeeId (FK)─┼── References USERS/PROFILES
                        │ employeeName    │
                        │ employeeSkills[]│
                        │ status          │◄── "pending" | "accepted" | "rejected"
                        │ appliedAt       │
                        │ reviewedBy (FK)─┼── PM who reviewed
                        │ reviewedAt      │
                        └─────────────────┘


       ┌─────────────────┐
       │     SKILLS      │ (Master Data - Read Only)
       ├─────────────────┤
       │ skillId (PK)    │
       │ name            │
       │ category        │
       └─────────────────┘
```

---

## 7. User Flow Diagrams

### 7.1 Employee User Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           EMPLOYEE USER FLOW                                  │
└──────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   SPLASH    │
                              │   SCREEN    │
                              └──────┬──────┘
                                     │
                            Check Auth Status
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
           ┌────────────────┐               ┌────────────────┐
           │     LOGIN      │◄─────────────►│    SIGNUP      │
           │    SCREEN      │               │    SCREEN      │
           └───────┬────────┘               │ (Select Role:  │
                   │                        │   Employee)    │
                   │                        └───────┬────────┘
                   │                                │
                   └───────────────┬────────────────┘
                                   │
                          Authenticated as Employee
                                   │
                                   ▼
                         ┌─────────────────┐
                         │    EMPLOYEE     │
                         │   DASHBOARD     │
                         └────────┬────────┘
                                  │
           ┌──────────────────────┼──────────────────────┐
           │                      │                      │
           ▼                      ▼                      ▼
  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
  │    PROFILE      │    │  VIEW PROJECTS  │    │ MY APPLICATIONS │
  │    SCREEN       │    │   (Browse All)  │    │  (Track Status) │
  ├─────────────────┤    └────────┬────────┘    └─────────────────┘
  │ • Edit Skills   │             │
  │ • Experience    │             ▼
  │ • Certifications│    ┌─────────────────┐
  │                 │    │ PROJECT DETAILS │
  │ ┌─────────────┐ │    └────────┬────────┘
  │ │ 🔘 ON BENCH │ │             │
  │ │ ⚪ WORKING  │ │             ▼
  │ └─────────────┘ │    ┌─────────────────┐
  │   Toggle Switch │    │ APPLY TO PROJECT│
  └─────────────────┘    └─────────────────┘
```

### 7.2 Project Manager User Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       PROJECT MANAGER USER FLOW                               │
└──────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   SPLASH    │
                              │   SCREEN    │
                              └──────┬──────┘
                                     │
                            Check Auth Status
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
           ┌────────────────┐               ┌────────────────┐
           │     LOGIN      │◄─────────────►│    SIGNUP      │
           │    SCREEN      │               │    SCREEN      │
           └───────┬────────┘               │ (Select Role:  │
                   │                        │ Project Manager│
                   │                        └───────┬────────┘
                   │                                │
                   └───────────────┬────────────────┘
                                   │
                       Authenticated as Project Manager
                                   │
                                   ▼
                         ┌─────────────────┐
                         │    MANAGER      │
                         │   DASHBOARD     │
                         └────────┬────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      │                           │                           │
      ▼                           ▼                           ▼
┌───────────────┐        ┌─────────────────┐        ┌─────────────────┐
│UPLOAD PROJECT │        │  MY PROJECTS    │        │SEARCH EMPLOYEES │
│  (PM ONLY)    │        │  (Edit/Delete)  │        │  (Filter By:)   │
├───────────────┤        └────────┬────────┘        ├─────────────────┤
│ • Title       │                 │                 │ • Skills        │
│ • Description │                 │                 │ • Bench Status  │◄── Key Filter
│ • Skills Req  │                 ▼                 │ • Experience    │
│ • Team Size   │        ┌─────────────────┐        │ • Location      │
│ • Duration    │        │VIEW APPLICATIONS│        └────────┬────────┘
└───────────────┘        │ (For Project)   │                 │
                         ├─────────────────┤                 ▼
                         │ ✅ Accept       │        ┌─────────────────┐
                         │ ❌ Reject       │        │ EMPLOYEE DETAIL │
                         └─────────────────┘        │   (Contact)     │
                                                    └─────────────────┘
```

### 7.3 Navigation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE NAVIGATION FLOW                             │
└─────────────────────────────────────────────────────────────────────────────┘

                            ┌─────────────┐
                            │   SPLASH    │
                            └──────┬──────┘
                                   │
                          Check Auth Status
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
     │     LOGIN      │   │    SIGNUP      │   │   LOGGED IN    │
     │    SCREEN      │◄─►│    SCREEN      │   │   (Redirect)   │
     └───────┬────────┘   └───────┬────────┘   └───────┬────────┘
             │                    │                    │
             └─────────┬──────────┘                    │
                       │                               │
               Authentication Success                  │
                       │                               │
              ┌────────┴────────┐                      │
              │  Check Role     │◄─────────────────────┘
              │                 │
              ▼                 ▼
    ┌─────────────────┐ ┌─────────────────┐
    │    EMPLOYEE     │ │    MANAGER      │
    │      HOME       │ │    DASHBOARD    │
    └────────┬────────┘ └────────┬────────┘
             │                   │
    ┌────────┴────────┐  ┌───────┴───────┬───────────────┐
    │                 │  │               │               │
    ▼                 ▼  ▼               ▼               ▼
┌────────┐    ┌────────┐ ┌────────┐ ┌────────────┐ ┌────────────┐
│PROFILE │    │ VIEW   │ │ UPLOAD │ │  SEARCH    │ │   VIEW     │
│ EDIT   │    │PROJECTS│ │PROJECT │ │ EMPLOYEES  │ │APPLICATIONS│
│+ BENCH │    └───┬────┘ └────────┘ └─────┬──────┘ └────────────┘
└────────┘        │                       │
                  ▼                       ▼
            ┌──────────┐           ┌──────────────┐
            │ PROJECT  │           │   EMPLOYEE   │
            │ DETAILS  │           │   DETAILS    │
            └────┬─────┘           └──────────────┘
                 │
                 ▼
            ┌──────────┐
            │  APPLY   │
            │(Employee)│
            └──────────┘
```

---

## 8. Data Models (Kotlin)

### 8.1 User.kt
```kotlin
package com.example.gladiator.data.model

/**
 * Represents a user's basic authentication data.
 * Stored in Firebase under /users/{uid}
 */
data class User(
    val uid: String = "",
    val email: String = "",
    val fullName: String = "",
    val role: String = "",          // "employee" | "project_manager"
    val createdAt: Long = System.currentTimeMillis()
)
```

### 8.2 UserRole.kt
```kotlin
package com.example.gladiator.data.model

/**
 * Enum defining user roles with type safety.
 */
enum class UserRole(val value: String) {
    EMPLOYEE("employee"),
    PROJECT_MANAGER("project_manager");

    companion object {
        fun fromString(role: String): UserRole? =
            entries.find { it.value == role }
    }
}
```

### 8.3 Profile.kt
```kotlin
package com.example.gladiator.data.model

/**
 * Represents an employee's detailed profile.
 * Stored in Firebase under /profiles/{uid}
 * 
 * Note: Only employees have profiles, not project managers.
 */
data class Profile(
    val uid: String = "",
    val experience: String = "",
    val location: String = "",
    val skills: List<String> = emptyList(),
    val projectHistory: List<String> = emptyList(),
    val certifications: List<String> = emptyList(),
    
    // ╔═══════════════════════════════════════╗
    // ║         BENCH STATUS FIELDS           ║
    // ║  Employee can toggle this themselves  ║
    // ╚═══════════════════════════════════════╝
    val isBenched: Boolean = false,        // TRUE = On Bench (Available)
                                           // FALSE = Currently Working
    val benchedSince: Long? = null,        // Timestamp when benched
    
    val profileImageUrl: String = "",
    val updatedAt: Long = System.currentTimeMillis()
)
```

### 8.4 Project.kt
```kotlin
package com.example.gladiator.data.model

/**
 * Represents a project requirement.
 * Stored in Firebase under /projects/{projectId}
 * 
 * IMPORTANT: Only Project Managers can create/edit/delete projects.
 */
data class Project(
    val projectId: String = "",
    val title: String = "",
    val description: String = "",
    
    // ╔═══════════════════════════════════════╗
    // ║    PROJECT MANAGER (OWNER) INFO       ║
    // ╚═══════════════════════════════════════╝
    val managerId: String = "",            // PM's user ID who created this
    val managerName: String = "",          // PM's display name
    
    val requiredSkills: List<String> = emptyList(),
    val experienceRequired: String = "",
    val teamSize: Int = 1,
    val location: String = "",
    val startDate: Long = 0L,
    val endDate: Long = 0L,
    val status: String = "open",           // "open" | "in_progress" | "closed"
    val createdAt: Long = System.currentTimeMillis()
)
```

### 8.5 Application.kt
```kotlin
package com.example.gladiator.data.model

/**
 * Represents an employee's application to a project.
 * Stored in Firebase under /applications/{applicationId}
 * 
 * Flow:
 * 1. Employee applies → status = "pending"
 * 2. PM reviews → status = "accepted" or "rejected"
 */
data class Application(
    val applicationId: String = "",
    val projectId: String = "",
    val employeeId: String = "",
    val employeeName: String = "",
    val employeeSkills: List<String> = emptyList(),
    val status: String = "pending",        // "pending" | "accepted" | "rejected"
    val appliedAt: Long = System.currentTimeMillis(),
    val reviewedBy: String = "",           // PM who reviewed
    val reviewedAt: Long? = null
)
```

### 8.6 Skill.kt
```kotlin
package com.example.gladiator.data.model

/**
 * Represents a skill in the master skills list.
 * Stored in Firebase under /skills/{skillId}
 * 
 * This is master data, typically read-only for users.
 */
data class Skill(
    val skillId: String = "",
    val name: String = "",
    val category: String = ""              // e.g., "Programming", "Framework", "Tool"
)
```

### 8.7 Resource.kt (Utility)
```kotlin
package com.example.gladiator.util

/**
 * A wrapper class for handling different states of data operations.
 * Used throughout the app for consistent state management.
 */
sealed class Resource<T>(
    val data: T? = null,
    val message: String? = null
) {
    class Success<T>(data: T) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
    class Loading<T>(data: T? = null) : Resource<T>(data)
}
```

---

## 9. Firebase Security Rules

```json
{
  "rules": {
    
    // ═══════════════════════════════════════════════════════════
    // USERS: Each user can only read/write their own data
    // ════════════════════════════════��══════════════════════════
    "users": {
      "$uid": {
        ".read": "auth != null",
        ".write": "auth != null && auth.uid == $uid"
      }
    },
    
    // ═══════════════════════════════════════════════════════════
    // PROFILES: Employee can edit own profile
    // Anyone authenticated can read (for PM to search)
    // ═══════════════════════════════════════════════════════════
    "profiles": {
      "$uid": {
        ".read": "auth != null",
        ".write": "auth != null && auth.uid == $uid"
      }
    },
    
    // ═══════════════════════════════════════════════════════════
    // PROJECTS: ONLY PROJECT MANAGERS CAN CREATE/EDIT/DELETE
    // All authenticated users can read
    // ═══════════════════════════════════════════════════════════
    "projects": {
      ".read": "auth != null",
      
      "$projectId": {
        // Only project_manager role can write
        // Can only edit if they are the owner (managerId matches)
        ".write": "auth != null && 
                   root.child('users').child(auth.uid).child('role').val() == 'project_manager' &&
                   (data.child('managerId').val() == auth.uid || !data.exists())"
      }
    },
    
    // ═══════════════════════════════════════════════════════════
    // APPLICATIONS: 
    // - Employee can create (apply)
    // - PM can update status (accept/reject)
    // ═══════════════════════════════════════════════════════════
    "applications": {
      ".read": "auth != null",
      
      "$appId": {
        ".write": "auth != null"
      }
    },
    
    // ═══════════════════════════════════════════════════════════
    // SKILLS: Master data - Read only
    // ═══════════════════════════════════════════════════════════
    "skills": {
      ".read": "auth != null",
      ".write": false
    }
  }
}
```

---

## 10. Screen Access Control

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SCREEN ACCESS MATRIX                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SCREEN                          │  EMPLOYEE  │  PROJECT MANAGER            │
│  ────────────────────────────────┼────────────┼─────────────────            │
│                                  │            │                             │
│  AUTHENTICATION                  │            │                             │
│  ├─ Splash Screen                │     ✅     │       ✅                    │
│  ├─ Login Screen                 │     ✅     │       ✅                    │
│  └─ Signup Screen                │     ✅     │       ✅                    │
│                                  │            │                             │
│  EMPLOYEE SCREENS                │            │                             │
│  ├─ Employee Dashboard           │     ✅     │       ❌                    │
│  ├─ Employee Profile (Edit)      │     ✅     │       ❌                    │
│  ├─ Toggle Bench Status          │     ✅     │       ❌                    │
│  ├─ View All Projects            │     ✅     │       ✅                    │
│  ├─ Project Details              │     ✅     │       ✅                    │
│  ├─ Apply to Project             │     ✅     │       ❌                    │
│  └─ My Applications              │     ✅     │       ❌                    │
│                                  │            │                             │
│  PROJECT MANAGER SCREENS         │            │                             │
│  ├─ Manager Dashboard            │     ❌     │       ✅                    │
│  ├─ Upload Project               │     ❌     │       ✅                    │
│  ├─ Edit/Delete Project          │     ❌     │       ✅                    │
│  ├─ My Projects                  │     ❌     │       ✅                    │
│  ├─ Search Employees             │     ❌     │       ✅                    │
│  ├─ Filter by Bench Status       │     ❌     │       ✅                    │
│  ├─ View Employee Details        │     ❌     │       ✅                    │
│  ├─ View Applications            │     ❌     │       ✅                    │
│  └─ Accept/Reject Applications   │     ❌     │       ✅                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. UI Components

### 11.1 BenchStatusToggle Component

```kotlin
package com.example.gladiator.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

/**
 * A toggle component for employees to set their bench status.
 * 
 * @param isBenched Current bench status (true = available, false = working)
 * @param onStatusChange Callback when status is toggled
 * @param modifier Optional modifier
 */
@Composable
fun BenchStatusToggle(
    isBenched: Boolean,
    onStatusChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = if (isBenched) 
                Color(0xFFE8F5E9)  // Light green when benched
            else 
                Color(0xFFFFF3E0)  // Light orange when working
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = "Availability Status",
                    fontWeight = FontWeight.Bold,
                    style = MaterialTheme.typography.titleMedium
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = if (isBenched) 
                        "🟢 On Bench - Available for Projects" 
                    else 
                        "🟠 Currently Working on a Project",
                    color = if (isBenched) 
                        Color(0xFF2E7D32)  // Dark green
                    else 
                        Color(0xFFE65100), // Dark orange
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            
            Switch(
                checked = isBenched,
                onCheckedChange = onStatusChange,
                colors = SwitchDefaults.colors(
                    checkedThumbColor = Color(0xFF4CAF50),
                    checkedTrackColor = Color(0xFFA5D6A7),
                    uncheckedThumbColor = Color(0xFFFF9800),
                    uncheckedTrackColor = Color(0xFFFFCC80)
                )
            )
        }
    }
}
```

### 11.2 ProjectCard Component

```kotlin
package com.example.gladiator.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.gladiator.data.model.Project

/**
 * A card component to display project summary.
 */
@Composable
fun ProjectCard(
    project: Project,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,
        modifier = modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = project.title,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = project.description,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 2
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Skills chips
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                project.requiredSkills.forEach { skill ->
                    SkillChip(skillName = skill)
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "Team Size: ${project.teamSize}",
                    style = MaterialTheme.typography.bodySmall
                )
                Text(
                    text = project.status.uppercase(),
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}
```

### 11.3 SkillChip Component

```kotlin
package com.example.gladiator.ui.components

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * A chip component to display a skill tag.
 */
@Composable
fun SkillChip(
    skillName: String,
    modifier: Modifier = Modifier
) {
    AssistChip(
        onClick = { },
        label = { 
            Text(
                text = skillName,
                style = MaterialTheme.typography.bodySmall
            )
        },
        modifier = modifier
    )
}
```

---

## 12. Summary

### 12.1 Technology Stack

| Component | Technology |
|-----------|------------|
| **Platform** | Android |
| **Language** | Kotlin |
| **UI Framework** | Jetpack Compose |
| **Architecture** | MVVM |
| **Backend** | Firebase Realtime Database |
| **Authentication** | Firebase Auth |
| **State Management** | StateFlow / LiveData |
| **Async Operations** | Kotlin Coroutines |
| **DI (Optional)** | Hilt / Koin |
| **Navigation** | Compose Navigation |

### 12.2 Feature Summary

| Feature | Employee | Project Manager |
|---------|----------|-----------------|
| **Create Account** | ✅ | ✅ |
| **Edit Own Profile** | ✅ | ✅ |
| **Toggle Bench Status** | ✅ | ❌ |
| **View Projects** | ✅ | ✅ |
| **Upload Project** | ❌ | ✅ |
| **Edit/Delete Project** | ❌ | ✅ |
| **Apply to Project** | ✅ | ❌ |
| **Search Employees** | ❌ | ✅ |
| **Filter by Benched** | ❌ | ✅ |
| **Accept/Reject Apps** | ❌ | ✅ |

### 12.3 Key Business Rules

1. **Role-Based Access:**
   - Users select their role during signup (Employee or Project Manager)
   - Role determines which screens and features are accessible

2. **Project Management:**
   - Only Project Managers can create, edit, and delete projects
   - Projects require skills, team size, and duration information

3. **Bench Status:**
   - Only Employees have profiles with bench status
   - Employee can toggle their own bench status (On Bench / Working)
   - Project Managers can filter employees by bench status when searching

4. **Application Process:**
   - Employees can apply to open projects
   - Project Managers can accept or reject applications
   - Application status: pending → accepted/rejected

---

## 📎 Appendix

### A. Sample Firebase Data

```json
{
  "users": {
    "user_emp_001": {
      "uid": "user_emp_001",
      "email": "john.doe@company.com",
      "fullName": "John Doe",
      "role": "employee",
      "createdAt": 1710000000000
    },
    "user_pm_001": {
      "uid": "user_pm_001",
      "email": "jane.smith@company.com",
      "fullName": "Jane Smith",
      "role": "project_manager",
      "createdAt": 1710000000000
    }
  },
  "profiles": {
    "user_emp_001": {
      "uid": "user_emp_001",
      "experience": "5 years",
      "location": "New York",
      "skills": ["Kotlin", "Android", "Jetpack Compose", "Firebase"],
      "projectHistory": ["Banking App", "E-Commerce App"],
      "certifications": ["AWS Certified Developer"],
      "isBenched": true,
      "benchedSince": 1709500000000,
      "profileImageUrl": "",
      "updatedAt": 1710000000000
    }
  },
  "projects": {
    "proj_001": {
      "projectId": "proj_001",
      "title": "Mobile Banking App",
      "description": "Build a secure mobile banking application with transaction features.",
      "managerId": "user_pm_001",
      "managerName": "Jane Smith",
      "requiredSkills": ["Kotlin", "Android", "Security"],
      "experienceRequired": "3+ years",
      "teamSize": 4,
      "location": "Remote",
      "startDate": 1710000000000,
      "endDate": 1720000000000,
      "status": "open",
      "createdAt": 1710000000000
    }
  },
  "applications": {
    "app_001": {
      "applicationId": "app_001",
      "projectId": "proj_001",
      "employeeId": "user_emp_001",
      "employeeName": "John Doe",
      "employeeSkills": ["Kotlin", "Android"],
      "status": "pending",
      "appliedAt": 1710100000000,
      "reviewedBy": "",
      "reviewedAt": null
    }
  },
  "skills": {
    "skill_001": {
      "skillId": "skill_001",
      "name": "Kotlin",
      "category": "Programming Language"
    },
    "skill_002": {
      "skillId": "skill_002",
      "name": "Jetpack Compose",
      "category": "Framework"
    }
  }
}
```

---

**End of Document**

*Document Version: 1.0*  
*Last Updated: March 11, 2026*
