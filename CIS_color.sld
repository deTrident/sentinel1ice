<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <se:Name>cis_SGRDRWA_20180312T1800Z_pl_a</se:Name>
    <UserStyle>
      <se:Name>cis_SGRDRWA_20180312T1800Z_pl_a</se:Name>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>81 Gray ice</se:Name>
          <se:Description>
            <se:Title>81 Gray ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>81</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>81</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>81</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#6b22cf</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>84 Gray ice</se:Name>
          <se:Description>
            <se:Title>84 Gray ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>84</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>84</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>84</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#6b22cf</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>85 Gray-white ice</se:Name>
          <se:Description>
            <se:Title>85 Gray-white ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>85</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>85</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>85</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ce34ee</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>87 Thin first year ice</se:Name>
          <se:Description>
            <se:Title>87 Thin first year ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>87</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>87</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>87</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#91cf00</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>91 Medium first year ice</se:Name>
          <se:Description>
            <se:Title>91 Medium first year ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>91</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>91</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>91</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#2fc600</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>93 Thick first year ice</se:Name>
          <se:Description>
            <se:Title>93 Thick first year ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>93</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>93</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>93</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#196a00</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>95 Old ice</se:Name>
          <se:Description>
            <se:Title>95 Old ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>95</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>95</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>95</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#a14d23</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>99 Open water</se:Name>
          <se:Description>
            <se:Title>99 Open water</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Or>
              <ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>99</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>99</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
              <ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="max">
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CB</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>CC</ogc:PropertyName>
                  </ogc:Function>
                </ogc:PropertyIsEqualTo>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>SC</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>99</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#86c2ff</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
