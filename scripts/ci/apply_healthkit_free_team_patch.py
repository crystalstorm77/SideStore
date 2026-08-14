#!/usr/bin/env python3
"""Add basic HealthKit support to the AltSign revision pinned by SideStore 0.6.3."""

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CAPABILITIES_ROOT = REPOSITORY_ROOT / "Dependencies" / "AltSign" / "AltSign" / "Capabilities"


def replace_once(path: Path, old: str, new: str) -> None:
    contents = path.read_text(encoding="utf-8")
    occurrences = contents.count(old)
    if occurrences != 1:
        raise RuntimeError(
            f"Expected exactly one matching block in {path}, found {occurrences}. "
            "The pinned AltSign source may have changed."
        )
    path.write_text(contents.replace(old, new), encoding="utf-8")


def main() -> None:
    header = CAPABILITIES_ROOT / "ALTCapabilities.h"
    implementation = CAPABILITIES_ROOT / "ALTCapabilities.m"

    replace_once(
        header,
        "extern ALTEntitlement const ALTEntitlementInterAppAudio;\n"
        "extern ALTEntitlement const ALTEntitlementIncreasedDebuggingMemoryLimit;",
        "extern ALTEntitlement const ALTEntitlementInterAppAudio;\n"
        "extern ALTEntitlement const ALTEntitlementHealthKit;\n"
        "extern ALTEntitlement const ALTEntitlementIncreasedDebuggingMemoryLimit;",
    )
    replace_once(
        header,
        "extern ALTFeature const ALTFeatureInterAppAudio;",
        "extern ALTFeature const ALTFeatureInterAppAudio;\n"
        "extern ALTFeature const ALTFeatureHealthKit;",
    )
    replace_once(
        implementation,
        'ALTEntitlement const ALTEntitlementInterAppAudio = @"inter-app-audio";\n'
        "ALTEntitlement const ALTEntitlementIncreasedDebuggingMemoryLimit",
        'ALTEntitlement const ALTEntitlementInterAppAudio = @"inter-app-audio";\n'
        'ALTEntitlement const ALTEntitlementHealthKit = @"com.apple.developer.healthkit";\n'
        "ALTEntitlement const ALTEntitlementIncreasedDebuggingMemoryLimit",
    )
    replace_once(
        implementation,
        'ALTFeature const ALTFeatureInterAppAudio = @"IAD53UNK2F";',
        'ALTFeature const ALTFeatureInterAppAudio = @"IAD53UNK2F";\n'
        'ALTFeature const ALTFeatureHealthKit = @"HK421J6T7P";',
    )
    replace_once(
        implementation,
        "    else if ([feature isEqualToString:ALTFeatureInterAppAudio])\n"
        "    {\n"
        "        return ALTEntitlementInterAppAudio;\n"
        "    }",
        "    else if ([feature isEqualToString:ALTFeatureInterAppAudio])\n"
        "    {\n"
        "        return ALTEntitlementInterAppAudio;\n"
        "    }\n"
        "    else if ([feature isEqualToString:ALTFeatureHealthKit])\n"
        "    {\n"
        "        return ALTEntitlementHealthKit;\n"
        "    }",
    )
    replace_once(
        implementation,
        "    else if ([entitlement isEqualToString:ALTEntitlementInterAppAudio])\n"
        "    {\n"
        "        return true;\n"
        "    }",
        "    else if ([entitlement isEqualToString:ALTEntitlementInterAppAudio])\n"
        "    {\n"
        "        return true;\n"
        "    }\n"
        "    else if ([entitlement isEqualToString:ALTEntitlementHealthKit])\n"
        "    {\n"
        "        return true;\n"
        "    }",
    )
    replace_once(
        implementation,
        "    else if ([entitlement isEqualToString:ALTEntitlementInterAppAudio])\n"
        "    {\n"
        "        return ALTFeatureInterAppAudio;\n"
        "    }",
        "    else if ([entitlement isEqualToString:ALTEntitlementInterAppAudio])\n"
        "    {\n"
        "        return ALTFeatureInterAppAudio;\n"
        "    }\n"
        "    else if ([entitlement isEqualToString:ALTEntitlementHealthKit])\n"
        "    {\n"
        "        return ALTFeatureHealthKit;\n"
        "    }",
    )

    print("Applied basic HealthKit support to SideStore 0.6.3 AltSign.")


if __name__ == "__main__":
    main()
