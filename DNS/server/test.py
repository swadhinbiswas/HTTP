# --- UNIT TESTS START HERE ---

class TestDNSFunctions(unittest.TestCase):

    def test_encode_decode_cycle(self):
        """Test that we can encode a domain and decode it back to the same string"""
        domain = "www.google.com"
        encoded = DNSfunctions.encode_domain_name(domain)
        decoded, _ = DNSfunctions.parse_domain_name(encoded, 0)
        self.assertEqual(domain, decoded)

    def test_encode_simple_domain(self):
        domain = "google.com"
        expected = b'\x06google\x03com\x00'
        self.assertEqual(DNSfunctions.encode_domain_name(domain), expected)

    def test_encode_root(self):
        self.assertEqual(DNSfunctions.encode_domain_name("."), b'\x00')

    def test_parse_compression(self):
        # "com" at offset 0
        part1 = b'\x03com\x00'
        # "google" + pointer to offset 0 (0xC000)
        part2 = b'\x06google\xc0\x00'

        data = part1 + part2
        # Start parsing at part2 (index 5)
        name, offset = DNSfunctions.parse_domain_name(data, 5)

        self.assertEqual(name, "google.com")
        self.assertEqual(offset, len(data))

# This block ensures tests run only when you execute this file directly
if __name__ == '__main__':
    unittest.main()
