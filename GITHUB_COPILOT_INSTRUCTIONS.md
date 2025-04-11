# GitHub Copilot Instructions for "Schwob aufm Sattl" Blog Project

## Project Overview
"Schwob aufm Sattl" is a blog focused on bikepacking, bike travel adventures, and outdoor experiences. The project uses:
- **Frontend**: Nuxt.js for Server-Side Rendering (SSR)
- **Backend**: FastAPI
- **Database**: PostgreSQL

## Todo Management
- Important project tasks and progress tracking are maintained in `TODO.md`
- After each chat session or completed task, mark the relevant items as complete in the TODO list
- If new requirements or tasks are identified, add them to the appropriate section in TODO.md
- Use the TODO list as a roadmap for development and to track overall project progress

## Key Features to Implement
1. Admin panel with secure authentication for adventure creation and management
2. Homepage with hero image and current/upcoming adventure highlight
3. Navigation with adventure selection
4. Pages for routes/tours, equipment, profiles, gallery, and social media
5. Image upload and management system
6. YouTube video embedding functionality
7. Database for storing adventures, texts, image paths, and related content

## Project Naming Conventions
- Use descriptive names for components, functions, and variables
- Follow standard Nuxt.js and FastAPI naming conventions
- Comment code appropriately, especially complex logic

## Database Structure Guidance
When implementing database models, focus on relationships between:
- Adventures/Tours
- Routes/Tracks
- Equipment items
- Profile information
- Gallery images
- Social media content

## Backend Architecture & Design Patterns
- Implement Dependency Injection pattern for all services and repositories
- Maintain strict separation of concerns with a clear layered architecture:
  - **Models**: Data structures representing database tables
  - **Repositories**: Handle database operations for a specific model
  - **Services**: Contain business logic for a specific domain
  - **Hooks**: Handle specific events or processes related to a model
- **Each database table should have its own dedicated file** for:
  - Model (one model per file in `app/models/`)
  - Schema (one schema per file in `app/schemas/`)
  - Repository
  - Service
  - API Router
- Create separate files for related concerns instead of combining them
- Use FastAPI's dependency system for injecting dependencies
- Implement proper exception handling with custom exceptions
- Configure Swagger/OpenAPI documentation with proper descriptions and examples
- Create reusable middleware for authentication, logging, and error handling
- Unit test each layer independently

## Documentation
- Create and maintain documentation alongside code development
- Document all APIs with detailed descriptions, parameters, and response examples
- Include setup instructions for development and production environments
- Document database schema changes and migration procedures
- Create user documentation for admin interface features
- Document architectural decisions and patterns used
- Keep documentation updated when implementing new features

## Frontend Architecture & Design Patterns
- Use Nuxt's Composition API with a component-based architecture
- Implement state management using Pinia with typed stores
- Follow Domain-Driven Design principles for frontend modules
- Create reusable components with proper prop validation
- Use a container/presentational component pattern:
  - Container components handle data fetching and state
  - Presentational components focus on UI rendering only
- Implement feature-based directory structure
- Create composables for shared logic
- Use TypeScript interfaces for all data models
- Implement responsive design with mobile-first approach
- **Use Vuetify as the UI framework** to minimize custom CSS/SCSS needs:
  - Vuetify provides a comprehensive set of pre-styled components
  - Has excellent Nuxt 3 integration
  - Offers Material Design aesthetics that work well for travel/adventure blogs
  - Includes built-in responsive grid system and layout components
  - Provides theming capabilities for customization

## Development Workflow
1. Consult the TODO.md before starting work on a new feature
2. Mark tasks as complete when finished
3. Add any new discovered tasks to the TODO list
4. Prioritize features based on the order in the TODO list

Remember that this is a personal travel/bikepacking blog with an emphasis on outdoor adventure content and an accessible admin interface for the blog owner.
