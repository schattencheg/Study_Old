using Moq;
using SteamKit;
using System;
using Xunit;

namespace SteamKit
{
    public class BotTests : IDisposable
    {
        private MockRepository mockRepository;



        public BotTests()
        {
            this.mockRepository = new MockRepository(MockBehavior.Strict);


        }

        public void Dispose()
        {
            this.mockRepository.VerifyAll();
        }

        private Bot CreateBot()
        {
            return new Bot();
        }

        [Fact]
        public void Run_StateUnderTest_ExpectedBehavior()
        {
            // Arrange
            var unitUnderTest = this.CreateBot();

            // Act
            unitUnderTest.Run();

            // Assert
            Assert.True(false);
        }
    }
}
