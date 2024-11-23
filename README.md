# AI Pull Request Reviewer 🤖

An intelligent pull request review system that leverages Dust AI to analyze code quality, style, and documentation.

## Features ✨

- Automated code review focusing on:
  - Naming conventions
  - Code style and quality
  - Indentation
  - Documentation
  - Test coverage
- GitHub integration
- Rate-limited AI analysis (max 10 calls)
- Clean Architecture with DDD principles

## Requirements 📋

- Python 3.11+
- Poetry for dependency management
- GitHub access token
- Dust API key

## Installation 🚀

1. Clone the repository:
```bash
git clone git@github.com:tehioant/AIReview.git
cd AIReview
```

2. Install dependencies:
```bash
just install-dependencies
```

3. Create `.env` file:
```env
DUST_API_KEY=your_dust_api_key
GITHUB_TOKEN=your_github_token
MAX_DUST_CALLS=10
```

## Usage 💡

Run the reviewer from command line:

```bash
poetry run python main.py --pr-id=123
```

## Architecture 🏗️

The project follows Clean Architecture and Domain-Driven Design principles:

```
aireview/
├── src/
|    ├── domain/          # Business logic and entities
|    ├── infrastructure/  # External services implementation
|    └──  application/     # Application services and DTOs
└── tests/          # Unit and integration tests
```

## Development 🛠️

1. Set up development environment:
```bash
just install-dependencies
```

2. Run tests:
```bash
just tests
```

3. Format code:
```bash
just lint
```

## Contributing 🤝

1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Dust AI for providing the code analysis capabilities
- GitHub API for pull request integration