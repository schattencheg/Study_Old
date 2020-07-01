using Moq;
using STMWPF;
using System;
using Xunit;

namespace STMWPF
{
    public class SteamDiscountTests : IDisposable
    {
        private MockRepository mockRepository;



        public SteamDiscountTests()
        {
            this.mockRepository = new MockRepository(MockBehavior.Strict);


        }

        public void Dispose()
        {
            this.mockRepository.VerifyAll();
        }

        private SteamDiscount CreateSteamDiscount()
        {
            return new SteamDiscount();
        }

        [Fact]
        public void TestMethod1()
        {
            // Arrange
            var unitUnderTest = this.CreateSteamDiscount();

            // Act

            // Assert
            Assert.True(false);
        }
    }
}
