# PyTorch TestInfra

The PyTorch TestInfra project is collection of infrastructure components that are
supporting the PyTorch CI/CD system. It also contains various PyTorch development tools
like linters.

## Getting started

Clone the repository:

```shell
$ git clone --recursive https://github.com/pytorch/test-infra
```

## Directories

```
├── aws                                  # Infra running in AWS
│   ├── lambda
│   └── websites                         # Several websites supported by TestInfra
│       ├── download.pytorch.org
│       └── metrics.pytorch.org
├── setup-ssh                            # SSH access setup to CI workers
├── stats                                # CI related stats committed automatically by a bot
├── terraform-aws-github-runner          # Terraform modules and templates used in CI
├── tools                                # Tools and scripts
|   ├── clang-tidy-checks
|   └── scripts
└── torchci                              # Code for hud.pytorch.org and our pytorch bots which run there
    └── pages
```

## Setting up your Dev environment to locally run hud.pytorch.org
See the [README.md in `torchci`](https://github.com/pytorch/test-infra/blob/main/torchci/README.md).

## Linting
We use [`lintrunner`](https://pypi.org/project/lintrunner/) for linting and
formatting. `torchci` also uses `yarn`.

## Join the PyTorch TestInfra community
See the [`CONTRIBUTING`](CONTRIBUTING.md) file for how to help out.

## License
PyTorch TestInfra is BSD licensed, as found in the [`LICENSE`](LICENSE) file.

## Privacy

This Action contacts Chainguard's licensing server to verify authorization. Connection metadata (IP address, GitHub repository identifier, timestamp, and any metadata encoded in the auth token) is transmitted to Chainguard, Inc. even if authorization is denied in accordance with our [Privacy Notice](https://www.chainguard.dev/legal/privacy-notice)
