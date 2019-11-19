from xml.etree import ElementTree
import csv
import Library
from distutils.version import LooseVersion, StrictVersion




namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}

def main():
    # POM_FILE="pom.xml"   

    trusted_deps = get_trusted_jars("jars.csv")

    package_check_res, version_check_res = get_pom_and_compare(POM_FILE, trusted_deps)

    print_res("The not trusted dependens list:", package_check_res)
    print_res("The trusted dependens but newer version list:", version_check_res)

def print_res(header, res):
    print("")
    print(header)
    for it in res:
        print(it)

def get_pom_and_compare(filepath, trusted_deps):
    POM_FILE = filepath 
    

    tree = ElementTree.parse(POM_FILE)
    root = tree.getroot()

    package_check_res = []
    version_check_res = []

    properties = root.find('.//xmlns:properties', namespaces=namespaces)


    deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
    for d in deps:
        groupId = d.find("xmlns:groupId", namespaces=namespaces)
        artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
        version = d.find("xmlns:version", namespaces=namespaces)

        if "zuora" in groupId.text:
            continue

        dep_colon = groupId.text + ":" + artifactId.text
        dep_dot = groupId.text + "." + artifactId.text
        
        dep_colon = dep_colon.lower()
        dep_dot = dep_dot.lower()

        found = False
        for k, v in trusted_deps.items():
            if dep_colon in k or dep_dot in k or artifactId.text.lower() in k:
                found = True
                if compare_version(properties, version, v):
                    version_check_res.append(dep_colon + ":" + get_version_value(properties, version) + " > " + v)
                break

        if not found:
            package_check_res.append(dep_colon)

    return package_check_res, version_check_res

def compare_version(properties, version, trusted_version):
    if version is None:
        return False

    if LooseVersion(get_version_value(properties, version)) > LooseVersion(trusted_version):
        return True

    return False

def get_version_value(properties, version):
    if "${" in version.text:
        version_name = version.text[2:-1]
        version_value = properties.find('xmlns:' + version_name, namespaces=namespaces)
        return version_value.text
    else:
        return version.text

def get_trusted_jars(filepath):
    dict = {}

    line = 0
    with open(filepath, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            dict[str(row[0]).lower()] = row[1]
            line += 1
    print("Read {} lines with {} valid depends.".format(line, len(dict)))
    return dict

if __name__ == "__main__":
    main()
