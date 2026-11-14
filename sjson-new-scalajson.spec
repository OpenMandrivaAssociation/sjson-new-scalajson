Name:		sjson-new-scalajson
Version:	0.10.1
Release:	1
Summary:	sjson-new ScalaJSON support
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/eed3si9n/sjson-new
Source0:	sjson-new-scalajson-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	scala = 2.13.16
BuildRequires:	sjson-new-core = 0.10.1
BuildRequires:	shaded-scalajson = 1.0.0.M4
BuildRequires:	shaded-jawn-parser = 1.3.2
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	python
BuildRequires:	sysjar
Requires:	mvn(org.scala-lang:scala-library) = 2.13.16
Requires:	mvn(com.eed3si9n:sjson-new-core_2.13) = 0.10.1
Requires:	mvn(com.eed3si9n:shaded-scalajson_2.13) = 1.0.0.M4
Requires:	mvn(com.eed3si9n:shaded-jawn-parser_2.13) = 1.3.2

%description
sjson-new-scalajson %{version} compiled for Scala 2.13.16. Zinc's util-logging
calls Converter.toJsonUnsafe. The build copy rewrites the shade imports. The
shipped sources stay unchanged. Nothing is downloaded.

%prep
%autosetup -n sjson-new-scalajson-%{version}
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s compile.sh
test -s check.sh
test -s support/scalajson/src/main/scala/sjsonnew/support/scalajson/unsafe/Converter.scala
test -s support/scalajson/src/main/scala/sjsonnew/support/scalajson/unsafe/Parser.scala
grep -F -q 'import shaded.scalajson.ast.unsafe._' support/scalajson/src/main/scala/sjsonnew/support/scalajson/unsafe/Parser.scala
grep -F -q 'import shaded.org.typelevel.jawn' support/scalajson/src/main/scala/sjsonnew/support/scalajson/unsafe/Parser.scala
grep -F -q 'def jnull()' support/scalajson/src/main/scala/sjsonnew/support/scalajson/unsafe/Converter.scala

%build
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./compile.sh

%install
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
test -s sjson-new-scalajson.jar
cat > sjson-new-scalajson.pom << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.eed3si9n</groupId>
  <artifactId>sjson-new-scalajson_2.13</artifactId>
  <version>%{version}</version>
  <name>sjson-new-scalajson</name>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.scala-lang</groupId>
      <artifactId>scala-library</artifactId>
      <version>2.13.16</version>
    </dependency>
    <dependency>
      <groupId>com.eed3si9n</groupId>
      <artifactId>sjson-new-core_2.13</artifactId>
      <version>0.10.1</version>
    </dependency>
    <dependency>
      <groupId>com.eed3si9n</groupId>
      <artifactId>shaded-scalajson_2.13</artifactId>
      <version>1.0.0.M4</version>
    </dependency>
    <dependency>
      <groupId>com.eed3si9n</groupId>
      <artifactId>shaded-jawn-parser_2.13</artifactId>
      <version>1.3.2</version>
    </dependency>
  </dependencies>
</project>
EOF
mkdir -p %{buildroot}
sysjar install --buildroot %{buildroot} \
	--artifact sjson-new-scalajson.pom:sjson-new-scalajson.jar \
	--file-name sjsonnew-scalajson-%{version} \
	--filelist .mfiles
test -s %{buildroot}%{_javadir}/sjsonnew-scalajson-%{version}.jar
grep -F -q '"version": "%{version}"' %{buildroot}/usr/share/sysjar/index/com.eed3si9n/sjson-new-scalajson_2.13.sysjar

%check
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./check.sh

%files -f .mfiles
%license LICENSE
